README

------

Software for CRUD options on VPCs


We are maintaining a database table for each of the above mentioned parameters in a per-tenant DB.


create_VPC script:

------------------

python create_VPC.py 

1. Customer is asked for his Tenant id.

2. Customer is prompted for the password

3. How many VPCs are required.



delete_vpc  script:

-------------------

python delete_vpc.py



1. Customer is asked for his Tenant id.

2. Which VPC customer wants to delete.



read_vpc:

---------

This will be reading all the details regarding vpc from the database.



update_vpc:

-----------

This will update any topology changes in the database file.






