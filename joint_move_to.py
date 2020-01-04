import sys
import numpy as np
import time
from indydcp_client import IndyDCPClient
bind_ip = "192.168.0.6"   
server_ip = "192.168.0.7"
robot_name = "NRMK-Indy7"
indy = IndyDCPClient(bind_ip, server_ip, robot_name) 
indy.connect()

print('sys.argv length:',len(sys.argv))
if len(sys.argv) < 7 : 
   quit()

q = np.array(sys.argv[1:7],dtype=float)

indy.joint_move_to(q)

while(indy.is_move_finished() == 0):

    time.sleep(0.1)

print("JOINT MOVE TO : \n"+str(indy.get_joint_pos()))
print("TASK MOVE TO : \n"+str(indy.get_task_pos()))
print("GET TORQUE : \n"+str(indy.get_torque()))
