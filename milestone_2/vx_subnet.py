import subprocess
import os
import sqlite3
import pandas as pd
conn = sqlite3.connect('database.db')
c = conn.cursor()

t_id = input("Enter the tenant ID:")
subnet = input("enter the subnet ID: ") #Assuming /24
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
    
    def __init__(self, t_id, subnet, s_vpc, d_vpc, s_gre, d_gre_ip, s_vx, vx_pair, vn_id):
        self.t_id = t_id
        self.subnet = subnet
        self.s_vpc = s_vpc
        self.d_vpc = d_vpc
        self.s_gre = s_gre
        self.d_gre_ip = d_gre_ip
        self.s_vx = s_vx
        self.vx_pair = vx_pair
        self.vn_id = vn_id
        
def vx_pairr(vxl):
    with conn:
        c.execute("INSERT INTO vx_pair VALUES (:t_id, :subnet, :s_vpc, :d_vpc, :s_gre, :d_gre_ip, :s_vx, :vx_pair, :vn_id)",
                 {'t_id':vxl.t_id,'subnet': vxl.subnet,'s_vpc':vxl.s_vpc, 'd_vpc': vxl.d_vpc, 's_gre': vxl.s_gre,'d_gre_ip': vxl.d_gre_ip,'s_vx': vxl.s_vx,'vx_pair':vxl.vx_pair,'vn_id': vxl.vn_id})
        

def get_gre_by_ip(gre_pair):
    c.execute("SELECT gre_ip FROM gre WHERE gretun=:gretun",{'gretun':gre_pair})
    return c.fetchall() 
        
c.execute("CREATE TABLE IF NOT EXISTS vx_pair (t_id text,subnet text, s_vpc text, d_vpc text,s_gre text,d_gre_ip text,s_vx text, vx_pair text, vn_id text)")
#asking for cloud
c.execute("SELECT nsi FROM vpc") #Displaying all the available namespaces
m = c.fetchall()
l = []
for i in m:
    (j,) = i
    l.append(j)
s = set(l)
s = sorted(s)
print(s)
lengt = len(s)
#print(lengt)

op = input("Enter the option that you want to create your subnet cloud: ")

nsi = "ns"+op+"_t"+t_id

ip = subnet.split("/")[0]
s_ip = ip.split(".")[0]

if nsi in s: 
    if1 = nsi+"-s"+s_ip+"_if1"
    if2 = nsi+"-s"+s_ip+"_if2"
    br = nsi+"-s"+s_ip+"_br"
    #vxlan_dev = nsi+"-"+"vxd"
#vxlan_id = To be written in the loop of vxlan  - t_id, 


    print(nsi)
    print(if1)
    print(if2)
    print(br)
    #print(vxlan_dev)

nsl = s
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
        s_vx = 'vxlan'+'_s'+s_ip+"_"+str(i+1)+"_"+str(p+1)+"_t"+t_id
        vx_pair = 'vxlan'+'_s'+s_ip+"_"+str(p+1)+"_"+str(i+1)+"_t"+t_id
        vn = str(i+1)+str(p+1)
        nv = str(p+1)+str(i+1)
        vn = int(vn)
        nv = int(nv)
        vn_id = min(vn,nv)
        gre_ip = str(i+11)+"."+str(i+11)+"."+str(k)+"."+"1"
        gre_pair = 'gre'+ str(p+1)+str(i+1)+"_t"+t_id
        #print(gre_pair)
        ((d_gre_ip,),) = get_gre_by_ip(gre_pair)
        #print(d_gre_ip)
        vxl =Vx_pair(t_id, subnet, s_vpc, d_vpc, s_gre, d_gre_ip, s_vx, vx_pair, vn_id)
        vx_pairr(vxl)
        
        

#creating a namespace for the subnet  -   attaching a namespace to an existing namespace
res = subprocess.check_output(["sudo","ip","netns","add",nsi])

#adding interfaces
res = subprocess.check_output(["sudo","ip","link","add",if1,"type","veth","peer","name",if2])
res = subprocess.check_output(["sudo","ip", "link", "set", if1, "netns", nsi])
res = subprocess.check_output(["sudo","ip", "link", "set", if2, "netns", nsc])

#adding ip address to veth pairs
res = subprocess.check_output(["sudo","ip","netns","exec",nsi,"ip","addr","add",ipa,"dev",if1])
res = subprocess.check_output(["sudo","ip","netns","exec",nsc,"ip","addr","add",gw,"dev",if2])

#Turning on veth pairs
res = subprocess.check_output(["sudo","ip","netns","exec",nsi,"ip","link","set","dev",if1,"up"])
res = subprocess.check_output(["sudo","ip","netns","exec",nsc,"ip","link","set","dev",if2,"up"])


# create bridge
res = subprocess.check_output(["sudo","ip","netns","exec",nsc,"brctl","addbr",br])

# veth pair to bridge
res = subprocess.check_output(["sudo","ip","netns","exec",nsc,"ip","link","add",if2,"type","veth","peer","name",br])

# ip addr to bridge, turn up
res = subprocess.check_output(["sudo","ip","netns","exec",nsc,"ip","addr","add",ip,"dev",br])
res = subprocess.check_output(["sudo","ifconfig",br,brip,if2,"netmask","255.255.255.0","up"])

# vxlan interfaces

    
    # get the endpoint of that vpc's interface ip - 1.1.1.1, 2.2.2.1 ----
    res = subprocess.check_output(["sudo","ip","netns","exec",nsc,"ip","link","add","name",s_vx,"type","vxlan","id",vn_id,"dev",s_gre,"remote",d_gre_ip,"dstport","4789"])
    res = subprocess.check_output(["sudo","ip","netns","exec",nsc,"ip","link","set","dev",vxlan,"up"])
    res = subprocess.check_output(["sudo","ip","netns","exec",nsc,"brctl","addif",br,vxlan])



conn.commit()
conn.close()

conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table';")
l = c.fetchall()
for table_name in l:
    #print(table_name)
    db = sqlite3.connect('database.db')
    table = pd.read_sql_query("SELECT * from %s" % table_name, db)
    print(table)

conn.close()
