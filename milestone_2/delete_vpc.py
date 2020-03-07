import sqlite3
import pandas as pd
import subprocess 
def remove_subnet(sub):
    with conn:
        c.execute("DELETE from subnet WHERE ip = :ip AND t_id = :t_id",
                  {'ip': sub.ip, 't_id': sub.t_id})
    
conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table';")
l = c.fetchall()
for table_name in l:
    #print(table_name)
    db = sqlite3.connect('database.db')
    table = pd.read_sql_query("SELECT * from %s" % table_name, db)
    print(table)

print("Existing VPC's: ")
print("1.New York")
print("2.Delhi")
print("3.Tokyo")
print("4.London")
print("5. All")
t = raw_input("Enter the Tenant ID: ")
a = raw_input("Enter the VPC that you want to delete: ")
nsi = "ns"+a+"_t"+t
print(nsi)

if a != "5":
    c.execute("SELECT nsi FROM vpc")
    m = c.fetchall()
    l = []
    for i in m:
        (j,) = i
        l.append(j)
    s = set(l)
    print(s)
    c.execute("DELETE from vpc WHERE nsi = :nsi",
              {'nsi': nsi})
    c.execute("DELETE from gre WHERE s_vpc = :nsi", 
              {'nsi': nsi})
    c.execute("DELETE from gre WHERE d_vpc = :nsi", 
              {'nsi': nsi})
    c.execute("DELETE from gre_pair WHERE s_vpc = :s_vpc",
              {'s_vpc':nsi})
    c.execute("DELETE from gre_pair WHERE d_vpc = :nsi", 
              {'nsi': nsi})
    conn.commit()

    #Deleting ALL VPC'S in the hypervisor - to be done

    #Deleting namespace
    subprocess.check_output(["sudo","ip","netns","del",nsi])
    #c.execute("DROP TABLE IF EXISTS gre;")
    #c.execute("DROP TABLE IF EXISTS vpc;")
    #c.execute("DROP TABLE IF EXISTS gre_pair;")
    #else:
      #  c.execute("SELECT * nsi FROM vpc")
    
c.execute("SELECT name FROM sqlite_master WHERE type='table';")
l = c.fetchall()
for table_name in l:
    #print(table_name)
    db = sqlite3.connect('database.db')
    table = pd.read_sql_query("SELECT * from %s" % table_name, db)
    print(table)

conn.close()
