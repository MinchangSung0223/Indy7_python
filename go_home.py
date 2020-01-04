import sys
print('sys.argv length:',len(sys.argv))

for arg in sys.argv: 
    print('arg value = ', arg) 

from indydcp_client import IndyDCPClient
bind_ip = "192.168.0.6"   
server_ip = "192.168.0.7"
robot_name = "NRMK-Indy7"
indy = IndyDCPClient(bind_ip, server_ip, robot_name) 
indy.connect()
indy.go_home()
indy.disconnect()

