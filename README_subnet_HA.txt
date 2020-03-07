README

------

Software for CRUD options on Subnets with High Availability


vx_subnet_HA script:

---------------------

python vx_subnet_HA.py 

1. Customer is asked for his Tenant id.

2. Customer is prompted for the password

3. Subnet id 


monitor script
--------------

python monitor.py


If a bridge is down in a subnet, for a given tenant, it triggers another script react_fail.py with vpc and subnet details.

react_fail script
-----------------

python react_fail.py <tenant_id> <vpc_namespace> <subnet id> <bridge name>

This script makes the backup bridge active. This involves five steps:

a) Ip address is removed from the primary interface of the customer container

b) The same ip address is added to the backup interface of the customer container

c) IP is removed from previously active bridge

d) IP of the previously active bridge is added to the backup bridge 

e) A default route is added to the VM



Now, the backup bridge becomes active and starts forwarding traffic.

