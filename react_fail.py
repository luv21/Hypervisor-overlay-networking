import subprocess
import os
import sqlite3
import pandas as pd
import sys

t_id = sys.argv[1]
vpc_ns = sys.argv[2]
subnet = sys.argv[3]
br = sys.argv[4]

database= 'database_t'+t_id+'.db'
conn = sqlite3.connect(database)

c = conn.cursor()

c.execute("SELECT s_vx FROM vx_pair WHERE s_vpc = :s_vpc AND subnet = :subnet",{'s_vpc':vpc_ns, 'subnet':subnet}) #Displaying all the available namespaces
m = c.fetchall()
l = []
for i in m:
    (j,) = i
    l.append(j)
vxset = set(l)
vxset = sorted(vxset)

s_ip =subnet.split(".")[0]
vm = vpc_ns+"-s"+s_ip+"_vm"
i_off=subnet.split("/")[0].split(".")
i_off[3] = vpc_ns.split("_")[0].strip("ns")
ipa = '.'.join(i_off)

brip = subnet.split("/")[0]
i_off = ipa.split(".")
i_off[3] = "11"+ vpc_ns.split("_")[0].strip("ns")
brip = '.'.join(i_off)

#if1= vpc_ns+"-s"+s_ip+"_if1"
#bk1 = vpc_ns+"-s"+s_ip+"_bk1"

if "_br" in br:
	br_bk = vpc_ns+"-s"+s_ip+"_bk"
	if1 = vpc_ns+"-s"+s_ip+"_if1"
	bk1 = vpc_ns+"-s"+s_ip+"_bk1"
elif "_bk" in br:
	br_bk = vpc_ns+"-s"+s_ip+"_br"
	if1 = vpc_ns+"-s"+s_ip+"_bk1"
	bk1 = vpc_ns+"-s"+s_ip+"_if1"
#br = vpc_ns+"-s"+s_ip+"_br" 
#br_bk = vpc_ns+"-s"+s_ip+"_bk"


subprocess.check_output(["sudo","docker","exec","--privileged",vm,"ip","addr","del",ipa+"/24","dev",if1])
subprocess.check_output(["sudo","docker","exec","--privileged",vm,"ip","addr","add",ipa+"/24","dev",bk1])
subprocess.check_output(["sudo","docker","exec","--privileged",vpc_ns,"ip","addr","del",brip+"/24","dev",br])
subprocess.check_output(["sudo","docker","exec","--privileged",vpc_ns,"ip","addr","add",brip+"/24","dev",br_bk])
subprocess.check_output(["sudo","docker","exec","--privileged",vm,"ip","route","add","default","via",brip])

for vx in vxset:
	subprocess.check_output(["sudo","docker","exec","--privileged",vpc_ns,"brctl","delif",br,vx])
	subprocess.check_output(["sudo","docker","exec","--privileged",vpc_ns,"brctl","addif",br_bk,vx])
