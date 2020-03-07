#! /bin/bash
sudo docker rm $(sudo docker ps -aq)
rtr=$(sudo docker run -itd --name ns25 ubuntu-network)

echo  "$rtr"

ipf=$(sudo docker exec --privileged ns25 sysctl -w net.ipv4.ip_forward=1)

echo "$ipf"
