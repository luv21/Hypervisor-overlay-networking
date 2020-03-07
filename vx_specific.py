import subprocess
import os
import sqlite3
import pandas as pd
import Tkinter as tk
from Tkinter import *

root = Tk()
root.title('Subnet')

t_id = tk.StringVar()
subnet = tk.StringVar()
#password = tk.StringVar()

titleLabel = tk.Label(root, text = 'Create Subnet')
titleLabel.pack()

NameLabel = tk.Label(root,text = 'Tenant ID')
NameLabel.pack()
NameEntry = tk.Entry(root, textvariable = t_id)
NameEntry.pack()

#passLabel = tk.Label(root,text = 'Password')
#passLabel.pack()
#passEntry = tk.Entry(root, textvariable = password, show = '*')
#passEntry.pack()

sLabel = tk.Label(root,text = 'Subnet ID')
sLabel.pack()
sEntry = tk.Entry(root, textvariable = subnet)
sEntry.pack()

calculateButton = tk.Button(root, text= 'Submit',command=root.destroy).pack()
root.mainloop()

t_id = t_id.get()
subnet = subnet.get()
#password = password.get()

#if password != 'password':
 #       print("***** wrong password try again*****")
  #      quit()


database= 'database_t'+t_id+'.db'
conn = sqlite3.connect(database)


#conn = sqlite3.connect('database.db')
c = conn.cursor()

ip = subnet.split("/")[0]
i = ip.split(".")
i[3] = "1"
ipa = '.'.join(i)  #- to be given to the subnet
i[3] = "5"
gw = '.'.join(i)  # - to be given to the gateway
i[3] = "19"
brip = '.'.join(i)  #- to be given to the bridge

class Vx_pair:
    """A tunnel class"""
    
    def __init__(self, t_id, subnet, s_vpc, d_vpc, s_gre, d_gre_ip, s_vx, vx_pair, vn_id,vm):
        self.t_id = t_id
        self.subnet = subnet
        self.s_vpc = s_vpc
        self.d_vpc = d_vpc
        self.s_gre = s_gre
        self.d_gre_ip = d_gre_ip
        self.s_vx = s_vx
        self.vx_pair = vx_pair
        self.vn_id = vn_id
	self.vm = vm
        
def vx_pairr(vxl):
    with conn:
        c.execute("INSERT INTO vx_pair VALUES (:t_id, :subnet, :s_vpc, :d_vpc, :s_gre, :d_gre_ip, :s_vx, :vx_pair, :vn_id, :vm)",
                 {'t_id':vxl.t_id,'subnet': vxl.subnet,'s_vpc':vxl.s_vpc, 'd_vpc': vxl.d_vpc, 's_gre': vxl.s_gre,'d_gre_ip': vxl.d_gre_ip,'s_vx': vxl.s_vx,'vx_pair':vxl.vx_pair,'vn_id': vxl.vn_id,'vm':vxl.vm})
        

def vx_pairr1(vxl):
    with conn:
        c.execute("INSERT INTO vx_pair1 VALUES (:t_id, :subnet, :s_vpc, :d_vpc, :s_gre, :d_gre_ip, :s_vx, :vx_pair, :vn_id, :vm)",
                 {'t_id':vxl.t_id,'subnet': vxl.subnet,'s_vpc':vxl.s_vpc, 'd_vpc': vxl.d_vpc, 's_gre': vxl.s_gre,'d_gre_ip': vxl.d_gre_ip,'s_vx': vxl.s_vx,'vx_pair':vxl.vx_pair,'vn_id': vxl.vn_id,'vm':vxl.vm})



def get_gre_by_ip(gre_pair):
    c.execute("SELECT gre_ip FROM gre WHERE gretun=:gretun",{'gretun':gre_pair})
    return c.fetchall() 
        
c.execute("CREATE TABLE IF NOT EXISTS vx_pair (t_id text,subnet text, s_vpc text, d_vpc text,s_gre text,d_gre_ip text,s_vx text, vx_pair text, vn_id text, vm text)")


c.execute("CREATE TABLE IF NOT EXISTS vx_pair1 (t_id text,subnet text, s_vpc text, d_vpc text,s_gre text,d_gre_ip text,s_vx text, vx_pair text, vn_id text, vm text)")




#asking for cloud
c.execute("SELECT nsi FROM vpc") #Displaying all the available namespaces
m = c.fetchall()
l = []
for i in m:
    (j,) = i
    l.append(j)
s = set(l)
s = sorted(s)
#print(s)
lengt = len(s)
#print(lengt)


for i,j in enumerate(s):
    print(i+1,":",j)

op = raw_input("Enter the namespace that you want to create your subnet(seperated by comma): ")
op = op.split(',')
print(op)

nspp = []
for i in op:
    nsp = "ns"+i+"_t"+t_id
    nspp.append(nsp)
print(nspp)


ip = subnet.split("/")[0]
s_ip = ip.split(".")[0]


nsl = s
for i,j in enumerate(s):
    for k in range(1,len(s)):
        p = k+1
        if p>len(nsl)-1:
            p = 1
        if p == i:
            p = 0
        s_vpc = nsl[i]
        d_vpc = nsl[p]
	vm = j+"-s"+s_ip+"_vm"
        #s_gre_ip = ipal[i]
        #d_gre_ip = ipal[p]
        s_gre = 'gre'+str(i+1)+str(p+1)+"_t"+t_id
        s_vx = 'vx'+'_s'+s_ip+"_"+str(i+1)+str(p+1)+"_t"+t_id
        vx_pair = 'vx'+'_s'+s_ip+"_"+str(p+1)+str(i+1)+"_t"+t_id
        vn = str(i+1)+str(p+1)
        nv = str(p+1)+str(i+1)
        vn = int(vn)
        nv = int(nv)
        vn_id = min(vn,nv)
        vn_id = s_ip + str(vn_id)
        gre_ip = str(i+11)+"."+str(i+11)+"."+str(k)+"."+"1"
        gre_pair = 'gre'+ str(p+1)+str(i+1)+"_t"+t_id
        #print(gre_pair)
        ((d_gre_ip,),) = get_gre_by_ip(gre_pair)
        #print(d_gre_ip)
        vxl =Vx_pair(t_id, subnet, s_vpc, d_vpc, s_gre, d_gre_ip, s_vx, vx_pair, vn_id,vm)
        vx_pairr(vxl)
	if s_vpc in nspp and d_vpc in nspp:
            vx_pairr1(vxl)
        
for i,j in enumerate(s):
    #print(i)
    vm = j+"-s"+s_ip+"_vm"
    if1 = j+"-s"+s_ip+"_if1"
    if2 = j+"-s"+s_ip+"_if2"
    br = j+"-s"+s_ip+"_br"
    ipa = subnet.split("/")[0]
    i_off = ipa.split(".")
    i_off[3] = str(i+1)
    ipa = '.'.join(i_off) #It is the VM ip - given to if1
    gw = subnet.split("/")[0]
    i_off = ipa.split(".")
    i_off[3] = "1"+str(i+1)
    gw = '.'.join(i_off)  #IP given to other end of veth pair, attached to bridge
    brip = subnet.split("/")[0]
    i_off = ipa.split(".")
    i_off[3] = "11"+str(i+1)
    brip = '.'.join(i_off) #L-3 interface IP - of the bridge
    vn_id = s_ip+str(vn_id)
    #print(ipa)        

    if j in nspp:
    	#creating a namespace for the subnet  -   attaching a namespace to an existing namespace
    
    	subprocess.check_output(["sudo","docker","run","-itd","--name", vm, "ubuntu-network"]) 

    	#adding interfaces

    	res = subprocess.check_output(["sudo","ip","link","add",if1,"type","veth","peer","name",if2])

    	pid_vm = subprocess.check_output(["sudo","docker","inspect","--format","'{{.State.Pid}}'", vm]) 
    	subprocess.check_output(["sudo","ip","link","set","netns",pid_vm.strip("\n'"),"dev",if1,"up"])

    	pid_j = subprocess.check_output(["sudo","docker","inspect","--format","'{{.State.Pid}}'", j]) 
    	subprocess.check_output(["sudo","ip","link","set","netns",pid_j.strip("\n'"),"dev",if2,"up"])

    	#adding ip address to veth pairs


    	subprocess.check_output(["sudo","docker","exec","--privileged",vm,"ip","addr","add",ipa+"/24","dev",if1])

    	#res = subprocess.check_output(["sudo","ip","netns","exec",j,"ip","addr","add",gw,"dev",if2])

    	# create bridge

    	subprocess.check_output(["sudo","docker","exec","--privileged",j,"brctl","addbr",br])

    	# veth pair to bridge

    	subprocess.check_output(["sudo","docker","exec","--privileged",j,"brctl","addif",br,if2])

    	# ip addr to bridge, turn up
    	subprocess.check_output(["sudo","docker","exec","--privileged",j,"ip","addr","add",brip+"/24","dev",br])
    	subprocess.check_output(["sudo","docker","exec","--privileged",j,"ip","link","set", "dev", br,"up"])
    	subprocess.check_output(["sudo","docker","exec","--privileged",vm,"ip","route","del","default"])
    	subprocess.check_output(["sudo","docker","exec","--privileged",vm,"ip","route","add","default","via",brip])

# vxlan interfaces
#Vxlan - loop


for i,j in enumerate(s):
    for k in range(1,len(l)):
        p = k+1
        if p>len(nsl)-1:
            p = 1
        if p == i:
            p = 0
        s_vpc = nsl[i]
        d_vpc = nsl[p]
        #s_gre_ip = ipal[i]
        #d_gre_ip = ipal[p]
        s_gre = 'gre'+str(i+1)+str(p+1)+"_t"+t_id
        s_vx = 'vx'+'_s'+s_ip+"_"+str(i+1)+str(p+1)+"_t"+t_id
        vx_pair = 'vx'+'_s'+s_ip+"_"+str(p+1)+str(i+1)+"_t"+t_id
        br = j+"-s"+s_ip+"_br"
        vn = str(i+1)+str(p+1)
        nv = str(p+1)+str(i+1)
        vn = int(vn)
        nv = int(nv)
        vn_id = min(vn,nv)
        vn_id  = s_ip+str(vn_id)
        gre_ip = str(i+11)+"."+str(i+11)+"."+str(k)+"."+"1"
        gre_pair = 'gre'+ str(p+1)+str(i+1)+"_t"+t_id
        ((d_gre_ip,),) = get_gre_by_ip(gre_pair)
   	
	if s_vpc in nspp and d_vpc in nspp:
        	# get the endpoint of that vpc's interface ip - 1.1.1.1, 2.2.2.1 ----

        	subprocess.check_output(["sudo","docker","exec","--privileged",s_vpc,"ip","link","add","name",s_vx,"type","vxlan","id",str(vn_id),"dev",s_gre,"remote",d_gre_ip.split('/')[0],"dstport","4789"])
        	subprocess.check_output(["sudo","docker","exec","--privileged",s_vpc,"ip","link","set","dev",s_vx,"up"])
		subprocess.check_output(["sudo","docker","exec","--privileged",s_vpc,"brctl","addif",br,s_vx])


conn.commit()
conn.close()

conn = sqlite3.connect(database)
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table';")
l = c.fetchall()
for table_name in l:
    if "vx_pair" not in table_name:
    	#print(table_name)
    	db = sqlite3.connect(database)
    	table = pd.read_sql_query("SELECT * from %s" % table_name, db)
    	print(table)

conn.close()
