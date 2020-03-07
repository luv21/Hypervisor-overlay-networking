import subprocess
import os
import sqlite3
import pandas as pd
import Tkinter as tk
from Tkinter import *

root = Tk()
root.title('VPC')

tid = tk.StringVar()
vpc = tk.StringVar()

password = tk.StringVar()
titleLabel = tk.Label(root, text = 'VPC Create')
titleLabel.pack()

NameLabel = tk.Label(root,text = 'Tenant ID')
NameLabel.pack()
NameEntry = tk.Entry(root, textvariable = tid)
NameEntry.pack()

passLabel = tk.Label(root,text = 'Password')
passLabel.pack()
passEntry = tk.Entry(root, textvariable = password, show = '*')
passEntry.pack()

vpcLabel = tk.Label(root,text = 'VPCs required')
vpcLabel.pack()
vpcEntry = tk.Entry(root, textvariable = vpc)
vpcEntry.pack()


calculateButton = tk.Button(root, text= 'Submit',command=root.destroy).pack()
root.mainloop()

vpc = vpc.get()
tid = tid.get()
#print(subnet)
#print(t_id)
#print(type(subnet))
#print(type(t_id))


#res = subprocess.check_output(["sudo","ip","netns","add","ns25"])  #-  creating a master router, it is already existing

class Vpc:
    """A vpc class"""

    def __init__(self, t_id, vpc_id, ipa, gw, if1, if2, nsi):
        self.t_id = t_id
        self.vpc_id = vpc_id
        self.ipa = ipa
        self.gw = gw
        self.if1 = if1
        self.if2 = if2
        self.nsi = nsi
        
class Tun:
    """A tunnel class"""
    
    def __init__(self, gretun, s_vpc, d_vpc, s_gre_ip, d_gre_ip, gre_ip, gre_pair):
        self.gretun = gretun
        self.s_vpc = s_vpc
        self.d_vpc = d_vpc
        self.s_gre_ip = s_gre_ip
        self.d_gre_ip = d_gre_ip
        self.gre_ip = gre_ip
        self.gre_pair = gre_pair
        
class Gre_pair:
    """A tunnel class"""
    
    def __init__(self, gretun, s_vpc, d_vpc, gre_pair, gre_pair_ip):
        self.gretun = gretun
        self.s_vpc = s_vpc
        self.d_vpc = d_vpc
        self.gre_pair = gre_pair
        self.gre_pair_ip = gre_pair_ip

def insert_vpc(vpc):
    with conn:
        c.execute("INSERT INTO vpc VALUES (:t_id, :vpc_id , :ipa , :gw , :if1 , :if2 , :nsi)",
                  {'t_id': vpc.t_id, 'vpc_id': vpc.vpc_id , 'ipa': vpc.ipa , 'gw': vpc.gw, 'if1': vpc.if1, 
                   'if2': vpc.if2, 'nsi': vpc.nsi})
        conn.commit()
        
def gre_tunnel(gre):
    with conn:
        c.execute("INSERT INTO gre VALUES (:gretun, :s_vpc, :d_vpc, :s_gre_ip, :d_gre_ip, :gre_ip, :gre_pair)",
                 {'gretun':gre.gretun,'s_vpc': gre.s_vpc, 'd_vpc':gre.d_vpc, 's_gre_ip':gre.s_gre_ip, 'd_gre_ip': gre.d_gre_ip, 'gre_ip':gre.gre_ip, 'gre_pair':gre_pair})


def gre_pairr(grp):
    with conn:
        c.execute("INSERT INTO gre_pair VALUES (:gretun, :s_vpc, :d_vpc, :gre_pair, :gre_pair_ip)",
                 {'gretun':grp.gretun,'s_vpc': grp.s_vpc, 'd_vpc':grp.d_vpc, 'gre_pair':grp.gre_pair, 'gre_pair_ip':grp.gre_pair_ip})
        
def get_gre_by_name(gretun):
    c.execute("SELECT gre_pair FROM gre WHERE gretun=:gretun",{'gretun':gretun})
    return c.fetchall()

def get_gre_by_ip(gre_pair):
    c.execute("SELECT gre_ip FROM gre WHERE gretun=:gretun",{'gretun':gre_pair})
    return c.fetchall() 


password = password.get()

if password != 'password':
        print("***** wrong password try again*****")
        quit()


database = 'database.db'
conn = sqlite3.connect(database)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS tenant (t_id text, password text)")
c.execute("INSERT INTO tenant VALUES (:t_id, :password)",{'t_id':tid,'password':password})
conn.commit()
conn.close()

database = 'database_t'+tid+'.db'
conn = sqlite3.connect(database)

c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS vpc (t_id text,vpc_id text,ipa text, gw text, if1 text, if2 text, nsi text)")
c.execute("CREATE TABLE IF NOT EXISTS gre (gretun text, s_vpc text, d_vpc text, s_gre_ip text, d_gre_ip text, gre_ip text, gre_pair text)")
c.execute("CREATE TABLE IF NOT EXISTS gre_pair (gretun text, s_vpc text, d_vpc text, gre_pair text, gre_pair_ip text)")
    
#adding interfaces
l_t = ["a","b","c","d","e","f","g"]
vpc = int(vpc)
l=l_t[:vpc]
t_id = tid            #raw_input("Choose your tenant ID: ")
nsl = []
ipal = []

for i,j in enumerate(l):
    
    vpc_id = i+1
    if1 = j+"1"+"_t"+t_id #a1,b1,c1,d1_t_1
    if2 = j+"25"+"_t"+t_id #a25,b25,c25,d25
    
    #creating a veth pair
    res = subprocess.check_output(["sudo","ip","link","add",if1,"type","veth","peer","name",if2])

    nsi = "ns"+str(i+1)+"_t"+t_id #ns1_t_1
    nsc = "ns25"
    nsl.append(nsi)
   # pid-nsi = "pid-"+str(i+1)+"-t"+t_id
    
    #creating namespace
    res = subprocess.check_output(["sudo","docker","run","-itd","--name",nsi,"ubuntu-network"])
    
    
    #pushing veth pairs to interfaces
    pid_nsi = subprocess.check_output(["sudo","docker","inspect","--format","'{{.State.Pid}}'",nsi])
    subprocess.check_output(["sudo","ip","link","set","netns",pid_nsi.strip("\n'"),"dev",if1,"up"])
    pid_nsc = subprocess.check_output(["sudo","docker","inspect","--format","'{{.State.Pid}}'",nsc])
    subprocess.check_output(["sudo","ip","link","set","netns",pid_nsc.strip("\n'"),"dev",if2,"up"])
    
    
    ipa = str(i+1)+"."+str(i+1)+"."+t_id+".1"+"/24"  # 1.1.1.1 , 2.2.2.1 , 3.3.3.1, 4.4.4.1
    gw = str(i+1)+"."+str(i+1)+"."+t_id+".25"+"/24"  # 1.1.1.25 , 2.2.2.25 , 3.3.3.25, 4.4.4.25
    gw_ip = str(i+1)+"."+str(i+1)+"."+t_id+".25"
    gr_ip = str(i+11)+"."+str(i+11)+"."+str(i+11)+"."+str(i+1)
    ipal.append(ipa)
    
    #giving ips to veth pairs
    subprocess.check_output(["sudo","docker","exec","--privileged",nsi,"ip","addr","add",ipa,"dev",if1])
    subprocess.check_output(["sudo","docker","exec","--privileged",nsc,"ip","addr","add",gw,"dev",if2])
    #res = subprocess.check_output(["sudo","ip","netns","exec",nsi,"ip","addr","add",ipa,"dev",if1])
    #res = subprocess.check_output(["sudo","ip","netns","exec",nsc,"ip","addr","add",gw,"dev",if2])
    
    #turning up veth pairs
    #res = subprocess.check_output(["sudo","ip","netns","exec",nsi,"ip","link","set","dev",if1,"up"])
    #res = subprocess.check_output(["sudo","ip","netns","exec",nsc,"ip","link","set","dev",if2,"up"])
     
    
    #adding default route
    #res= subprocess.check_output(["sudo","ip","netns","exec",nsi,"ip","route","add","default","via",gw_ip])
    subprocess.check_output(["sudo","docker","exec","--privileged",nsi,"ip","route","del","default"])
    subprocess.check_output(["sudo","docker","exec","--privileged",nsi,"ip","route","add","default","via",gw_ip])
    vpc1 = Vpc(t_id, vpc_id, ipa, gw, if1, if2, nsi)
    insert_vpc(vpc1)

    
for i,j in enumerate(l):
    for k in range(1,len(l)):
        
        # gre interfaces - to be written in the vpc ********
        
        s_vpc = nsl[i]
        p = k+1
        if p>len(nsl)-1:
            p = 1
        if p == i:
            p = 0
        d_vpc = nsl[p]
        s_gre_ip = ipal[i]
        d_gre_ip = ipal[p]
        gretun = 'gre'+str(i+1)+str(p+1)+"_t"+t_id
        gre_pair = 'gre'+ str(p+1)+str(i+1)+"_t"+t_id
        gre_ip = str(i+11)+"."+str(i+11)+"."+str(k)+"."+"1/24" 
        gre1 = Tun(gretun, s_vpc, d_vpc, s_gre_ip, d_gre_ip, gre_ip, gre_pair)
        gre_tunnel(gre1)
        # -----add ip address to gre device
        
        #print(nsl[i])
        res = subprocess.check_output(["sudo","docker","exec","--privileged",nsl[i],"ip","tunnel","add",gretun,"mode","gre","local",s_gre_ip.split('/')[0],"remote",d_gre_ip.split('/')[0]])
        res = subprocess.check_output(["sudo","docker","exec","--privileged",nsl[i],"ip","addr","add",gre_ip,"dev",gretun])
        res = subprocess.check_output(["sudo","docker","exec","--privileged",nsl[i],"ip","link","set","dev",gretun,"up"])
   
        
        
for i,j in enumerate(l):
    for k in range(1,len(l)):
        p = k+1
        if p>len(nsl)-1:
            p = 1
        if p == i:
            p = 0
        s_vpc = nsl[i]
        d_vpc = nsl[p]
        s_gre_ip = ipal[i]
        d_gre_ip = ipal[p]
        gretun = 'gre'+str(i+1)+str(p+1)+"_t"+t_id
        gre_pair = 'gre'+ str(p+1)+str(i+1)+"_t"+t_id
        ((p,),) = get_gre_by_name(gretun)
        #print(p)
        ((gre_pair_ip,),) = get_gre_by_ip(p)
        gre_pair_ip = gre_pair_ip.split('/')[0]
        li = gre_pair_ip.split('.')
        li[3] = '0/24'
        gre_pair_ip = '.'.join(li)
        gre_pair1 = Gre_pair(gretun, s_vpc, d_vpc, gre_pair, gre_pair_ip)
        gre_pairr(gre_pair1)
        
        res = subprocess.check_output(["sudo","docker","exec","--privileged",nsl[i],"ip","route","add",gre_pair_ip,"dev",gretun])


conn = sqlite3.connect(database)
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table';")
l = c.fetchall()
for table_name in l:
    #print(table_name)
    db = sqlite3.connect(database)
    table = pd.read_sql_query("SELECT * from %s" % table_name, db)
    print(table)

#c.execute("DROP TABLE IF EXISTS gre;")
#c.execute("DROP TABLE IF EXISTS vpc;")
#c.execute("DROP TABLE IF EXISTS gre_pair;")
conn.commit()
conn.close()
