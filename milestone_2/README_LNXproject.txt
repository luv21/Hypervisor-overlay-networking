README
------
The software employs CRUD model. We use this for the operations on VPCs, their subnets and the tunnels.

Deliverables:
------------
CRUD (Create, Read, Update, Delete) for:
	1. VPC 
	2. Subnets
	3. Tunnels(VxLAN and GRE both)

We are maintaining a database table for each of the above mentioned parameters. 

For the read operation, we are just going to read out of the database.

Dependencies to be imported:
---------------------------
os
subprocess
sqlite3
pandas
Tkinter
*Path to the database file must be known by the user and input into the code.  


Execution:
----------
1. The first step to execution is that the user is presented with a form.
2. This form has options for a custom as well as a default topology in case user does not have idea about his topology design.
 - Default config has 4 VPCs, 4 subnets(one per VPC), and 12 tunnels.
 - Custom config gives the user freedom to design his own topology. He can specify the number of VPCs he wants, the subnets he wants in them. The tunnels in them will     be (n*n-1) where n is the number of VPCs.
   Each VPC will contain VxLAN and GRE tunnel endpoints. Whether to use it or no depends on the use-case. 
   If there are (n) number of VPCs in a topology, then in a single VPC, the number of GRE tunnel endpoints are (n-1). Also, if there are (m) number of subnets per VPC,    then the total number of VxLAN endpoints are (m*n-1)

create_vpc script:
------------------

<python create_vpc>

1. Customer is asked for his Tenant id.
2. How many VPCs are required.

delete_vpc  script:
-------------------

<python delete_vpc>

1. Customer is asked for his Tenant id.
2. Which VPC customer wants to delete.


read_vpc:
---------
This will be storing all the details regarding vpc in the database.

update_vpc:
-----------
This will update any topology changes in the database file.


Similarly, this can be extended for subnets and tunnels of the customer.