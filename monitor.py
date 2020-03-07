#!/usr/bin/python
import os
import subprocess
import sys
import sqlite3
import pandas as pd

subprocess.check_output(["echo","1", ">>","test.txt"])
database = 'database.db'
conn = sqlite3.connect(database)
subprocess.check_output(["echo","2.5", ">>","test.txt"])

c = conn.cursor() 
c.execute("SELECT t_id FROM tenant") 
m = c.fetchall()
l = []
for i in m:
    (j,) = i
    l.append(j)
t_ids = set(l)
t_ids = sorted(t_ids)
print(t_ids)

for t_id in t_ids:

	database= 'database_t'+t_id+'.db'
	conn = sqlite3.connect(database)

	c = conn.cursor()


	c.execute("SELECT nsi FROM vpc") #Displaying all the available namespaces
	m = c.fetchall()
	l = []
	for i in m:
	    (j,) = i
	    l.append(j)
	s_nsi = set(l)
	s_nsi = sorted(s_nsi)

	c.execute("SELECT subnet FROM vx_pair") #Displaying all the available subnets
	m = c.fetchall()
	l = []
	for i in m:
	    (j,) = i
	    l.append(j)
	s_sub = set(l)
	s_sub = sorted(s_sub)



	for i,ns in enumerate(s_nsi):     #looping for subnets?
	# ns = "ns1_t34"
	  for j,sub in enumerate(s_sub):
		 sub1 = sub.split('.')
		 sub1 = sub1[0]
	 	 br =  ns+"-s"+sub1+"_br"
		 br_bk = ns+"-s"+sub1+"_bk"


  		 state_br = subprocess.check_output(["sudo","docker","exec","--privileged",ns,"cat","/sys/class/net/"+br+"/operstate"])
	       	 state_bk = subprocess.check_output(["sudo","docker","exec","--privileged",ns,"cat","/sys/class/net/"+br_bk+"/operstate"])
		 #print(state.strip())
	 
	  	 if(state_br.strip()=="down"):
	    	 	subprocess.check_output(["sudo","python","react_fail.py",t_id,ns,sub,br])
		 elif(state_bk.strip()=="down"):
	                subprocess.check_output(["sudo","python","react_fail.py",t_id,ns,sub,br_bk])




subprocess.check_output(["echo","3", ">>","test.txt"])

