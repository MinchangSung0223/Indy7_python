import sys
import argparse
from PIL import Image
from primesense import openni2  # , nite2
from primesense import _openni2 as c_api
from matplotlib import pyplot as plt
import time
import numpy as np
import cv2
import threading
from ctypes import cdll
import ctypes
from numpy.ctypeslib import ndpointer
lib = cdll.LoadLibrary('./viewer_opengl.so')
import math
st = lib.Foo_start
t0 = threading.Thread(target=st)
t0.start()
end = lib.Foo_end
dataread =lib.Foo_dataread
dataread_color =lib.Foo_dataread_color
dataread_depth =lib.Foo_dataread_depth
dataread_color_to_depth =lib.Foo_dataread_color_to_depth
dataread.restype = ndpointer(dtype=ctypes.c_uint8, shape=(720,1280,2))
dataread_color.restype = ndpointer(dtype=ctypes.c_uint8, shape=(720,1280,4))
dataread_depth.restype = ndpointer(dtype=ctypes.c_uint16, shape=(512,512))#ctypes.POINTE
dataread_color_to_depth.restype = ndpointer(dtype=ctypes.c_uint8, shape=(512,512,4))

from indydcp_client import IndyDCPClient
bind_ip = "192.168.0.6"   
server_ip = "192.168.0.7"
robot_name = "NRMK-Indy7"
indy = IndyDCPClient(bind_ip, server_ip, robot_name) 
indy.connect()
def capture_img():
   global img 
   n = 0
   while 1:
      print("Press Enter")
      dd = input()
      pos = np.array(indy.get_task_pos(),dtype=float)
      T = np.zeros((4,4),dtype=float)
      Rz = np.zeros((3,3),dtype=float)
      Ry = np.zeros((3,3),dtype=float)
      Rx = np.zeros((3,3),dtype=float)

      Rz[0,0] = math.cos(pos[5]/180*math.pi)
      Rz[0,1] = -math.sin(pos[5]/180*math.pi)
      Rz[1,0] = math.sin(pos[5]/180*math.pi)
      Rz[1,1] = math.cos(pos[5]/180*math.pi)
      Rz[2,2] = 1

      Ry[0,0] = math.cos(pos[4]/180*math.pi)
      Ry[0,2] = math.sin(pos[4]/180*math.pi)
      Ry[2,0] = -math.sin(pos[4]/180*math.pi)
      Ry[2,2] = math.cos(pos[4]/180*math.pi)
      Ry[1,1] = 1
 
      Rx[1,1] = math.cos(pos[3]/180*math.pi)
      Rx[1,2] = -math.sin(pos[3]/180*math.pi)
      Rx[2,1] = math.sin(pos[3]/180*math.pi)
      Rx[2,2] = math.cos(pos[3]/180*math.pi)
      Rx[0,0] = 1
      print(Rz)
      print(Ry)
      print(Rx)

      R = np.matmul(np.matmul(Rz,Ry),Rx)

      T[0:3,0:3] =R
      T[0,3] =pos[0]
      T[1,3] =pos[1]
      T[2,3] =pos[2]
      T[3,3] =1

      filename = "pose_"+str(n)+".png"
      filenamepos = "pose_"+str(n)+".txt"

      n = n+1
      print(T)
      np.savetxt(filenamepos,T)
      cv2.imwrite(filename, img)
      print("SAVE "+filename)
      

   end()
   indy.finish_direct_teaching()
   indy.disconnect()
  

def show_img():
    global img 
    cv2.namedWindow('rgb', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('rgb', 1280,720)
    while True:
      try:
        try:
          color_data = np.array(dataread_color(),dtype=np.uint8)
          color_img = color_data[:,:,0:3]
          img = cv2.cvtColor(color_img.copy(),cv2.COLOR_BGR2RGB)
          img = cv2.cvtColor(img.copy(),cv2.COLOR_RGB2BGR)
          cv2.imshow('rgb',np.uint8(img))
          cv2.waitKey(1)
          time.sleep(0.01)
        except:
          print("error")
          pass

      except:
        end()
        indy.finish_direct_teaching()
        indy.disconnect()

FLAGS = None

if __name__ == '__main__':
    t1 = threading.Thread(target=show_img)
    t1.start()
    t2= threading.Thread(target=capture_img)
    t2.start()
    indy.change_to_direct_teaching()
  

