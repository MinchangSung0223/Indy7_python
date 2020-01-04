import sys
print('sys.argv length:',len(sys.argv))

for arg in sys.argv: 
    print('arg value = ', arg) 

from indydcp_client import IndyDCPClient
bind_ip = "166.104.206.154"   
server_ip = "166.104.206.76"
robot_name = "NRMK-Indy5"
indy = IndyDCPClient(bind_ip, server_ip, robot_name) 
indy.connect()
indy.go_home()
print("INDY CONNECTION : "+str(indy.is_connected()))
