from indydcp_client import IndyDCPClient
import sys
import numpy as np
import time
import math
bind_ip = "192.168.0.6"   
server_ip = "192.168.0.7"
robot_name = "NRMK-Indy7"
indy = IndyDCPClient(bind_ip, server_ip, robot_name) 
indy.connect()
print("INDY CONNECTION : "+str(indy.is_connected()))
th = 0
r = 0.1
indy.set_task_boundary_level(9)
indy.set_task_blend_radius(200)
while 1:
    th = th+0.005
    x = 0.5+r*math.cos(th)
    y = 0.0+r*math.sin(th)
    z = 0.5
    roll = math.atan(z/r)*180/math.pi*math.sin(th)
    pitch =math.atan(z/r)*180/math.pi*math.cos(th) 
    print(roll)
    print(pitch/4-180)
    indy.task_move_to([x,y,z,roll/4,pitch/8-180,0])
    

