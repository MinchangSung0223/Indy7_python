import sys
import numpy as np
import time
import math
from indydcp_client import IndyDCPClient
bind_ip = "192.168.0.6"   
server_ip = "192.168.0.7"
robot_name = "NRMK-Indy7"
indy = IndyDCPClient(bind_ip, server_ip, robot_name) 
indy.connect()

th = 0
r = 0.17
indy.set_task_boundary_level(9)
indy.set_task_blend_radius(200)
while 1:
    th = th+0.02
    x = 0.45+r*math.cos(th)
    y = 0.0+r*math.sin(th)
    z = 0.3
    roll = math.atan(z/r)*180/math.pi*math.sin(th)
    pitch =math.atan(z/r)*180/math.pi*math.cos(th) 
    print(roll)
    print(pitch/4-180)
    indy.task_move_to([x,y,z,roll/4,pitch/3-180,0])
    

