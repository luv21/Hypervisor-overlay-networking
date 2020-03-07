import pandas as pd
import sqlite3
import subprocess
import os


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



t_id = raw_input("Enter your tenant ID: ")

database = 'database_t'+t_id+'.db'
conn = sqlite3.connect(database)

c = conn.cursor()

conn = sqlite3.connect(database)
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table';")
l = c.fetchall()
for table_name in l:
    print(table_name)
    if "vx_pair" not in table_name:
        db = sqlite3.connect(database)
        table = pd.read_sql_query("SELECT * from %s" % table_name, db)
        print(table)

c.execute("DROP TABLE IF EXISTS vx_pair1")
c.execute("CREATE TABLE IF NOT EXISTS vx_pair1 (t_id text,subnet text, s_vpc text, d_vpc text,s_gre text,d_gre_ip text,s_vx text, vx_pair text, vn_id text, vm text)")


svpc = raw_input("Enter the source vpc: ")
subnet = raw_input("Enter the subnet to be migrated: ")
dvpc = raw_input("Enter the dest vpc:")


so_vpc = "ns"+svpc+"_t"+t_id
do_vpc = "ns"+dvpc+"_t"+t_id



ip = subnet.split("/")[0]
s_ip = ip.split(".")[0]

c.execute("SELECT nsi FROM vpc") #Displaying all the available namespaces
m = c.fetchall()
l = []
for i in m:
    (j,) = i
    l.append(j)
s = set(l)
s = sorted(s)
#print(s)

a = {1,2,3}
b = {int(svpc),int(dvpc)}
dov1 = a-b

for i in dov1:
	dov1 = i

do_v1 = "ns"+str(dov1)+"_t"+t_id

#The bridge present in so_vpc
BR = so_vpc+"-s"+s_ip+"_br"
VX_LAN = "vx_s"+s_ip+"_"+str(svpc)+str(dov1)+"_t"+t_id
VX_LAN2 = "vx_s"+s_ip+"_"+str(dov1)+str(svpc)+"_t"+t_id

#deleting subnet in svpc
subprocess.check_output(["sudo","docker","exec","--privileged",so_vpc,"ip","link","set",BR,"down"])
subprocess.check_output(["sudo","docker","exec","--privileged",so_vpc,"brctl","delbr",BR])
subprocess.check_output(["sudo","docker","exec","--privileged",so_vpc,"ip","link","del","dev",VX_LAN])




#deleting tunnel in dvpc
subprocess.check_output(["sudo","docker","exec","--privileged",do_v1,"ip","link","del","dev",VX_LAN2])


#crating a subnet
nsl = [so_vpc,do_vpc,do_v1]
nsl.sort()
#print(nsl)

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
	if j in d_vpc:
        	vm = so_vpc+"-s"+s_ip+"_vm"
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
        #vx_pairr(vxl)
	#print(s_vpc,d_vpc)
        if do_vpc in s_vpc and do_v1 in d_vpc:
            vx_pairr1(vxl)
	if do_v1 in s_vpc and  do_vpc in d_vpc:
	    vx_pairr1(vxl)


for i,j in enumerate(s):
    #print(i)
    vm = j+"-s"+s_ip+"_vm"
    if1 = j+"-s"+s_ip+"_if1"
    if2 = j+"-s"+s_ip+"_if2"
    br = j+"-s"+s_ip+"_br"
    ipa = subnet.split("/")[0]
    i_off = ipa.split(".")
    i_off[3] = str(svpc)
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

    if j == do_vpc:
	#print(ipa)
	
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

        #ip addr to bridge, turn up
        subprocess.check_output(["sudo","docker","exec","--privileged",j,"ip","addr","add",brip+"/24","dev",br])
        subprocess.check_output(["sudo","docker","exec","--privileged",j,"ip","link","set", "dev", br,"up"])
        subprocess.check_output(["sudo","docker","exec","--privileged",vm,"ip","route","del","default"])
        subprocess.check_output(["sudo","docker","exec","--privileged",vm,"ip","route","add","default","via",brip])

	print("")

for i,j in enumerate(s):
    for k in range(1,len(s)):
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

        if do_v1 in s_vpc and  do_vpc in d_vpc:
		#print(s_vpc,d_vpc)
               # get the endpoint of that vpc's interface ip - 1.1.1.1, 2.2.2.1 ----

                subprocess.check_output(["sudo","docker","exec","--privileged",s_vpc,"ip","link","add","name",s_vx,"type","vxlan","id",str(vn_id),"dev",s_gre,"remote",d_gre_ip.split('/')[0],"dstport","4789"])
                subprocess.check_output(["sudo","docker","exec","--privileged",s_vpc,"ip","link","set","dev",s_vx,"up"])
                subprocess.check_output(["sudo","docker","exec","--privileged",s_vpc,"brctl","addif",br,s_vx])
        if do_vpc in s_vpc and do_v1 in d_vpc:
		#print(s_vpc,d_vpc)
                # get the endpoint of that vpc's interface ip - 1.1.1.1, 2.2.2.1 ----

                subprocess.check_output(["sudo","docker","exec","--privileged",s_vpc,"ip","link","add","name",s_vx,"type","vxlan","id",str(vn_id),"dev",s_gre,"remote",d_gre_ip.split('/')[0],"dstport","4789"])
                subprocess.check_output(["sudo","docker","exec","--privileged",s_vpc,"ip","link","set","dev",s_vx,"up"])
                subprocess.check_output(["sudo","docker","exec","--privileged",s_vpc,"brctl","addif",br,s_vx])


conn.commit()



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

