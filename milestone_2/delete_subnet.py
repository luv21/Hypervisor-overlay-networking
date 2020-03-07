import subprocess
import os
import sqlite3
import pandas as pd
conn = sqlite3.connect('database.db')
c = conn.cursor()
def get_br_by_subnet(subnet_id,nsi):
    c.execute("SELECT * FROM vx_lan WHERE subnet_id=:subnet_id AND nsi = :nsi",{'subnet_id',subnet_id},{'nsi','nsi'])
    return c.fetchall() 

tid=raw_input("Enter the tenant id\n")
sub=raw_input("Enter the tenant id\n")
ns=raw_input("Enter the tenant id\n")
br = get_br_by_subnet(sub,ns+'_'+tid)
nsi = "ns"+str(ns)
conn.close()


subprocess.check_output(["sudo","ip","netns",nsi,"exec","brctl","delbr",br])

