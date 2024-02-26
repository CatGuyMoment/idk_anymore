import numpy as np
import bpy
import matplotlib.pyplot as plt
import mathutils
import math
import time
import os
from tqdm import tqdm

FILEPATH = "import.blend"
RESOLUTION = 0.02
GRAPHSIZE = 4
ANGLE_IN_RADIANS = np.pi/6 #default: 30 degrees


assert os.path.isfile(FILEPATH), f"You forgot to add a .blend file at {os.getcwd()}\\{FILEPATH}, silly!"


def calcArc(x,y,z,step):
    return (z*np.sqrt(  ((step-x)/z)**2+1)/np.cos(ANGLE))+y

def lerp(a,b,t):
    return a + (b-a)*t

def lerpVector3(first,second,t):
    x,y,z = lerp(first.x,second.x,t),lerp(first.y,second.y,t),lerp(first.z,second.z,t)
    return mathutils.Vector((x,y,z))


bpy.ops.wm.open_mainfile(filepath=FILEPATH)
plt.figure(figsize=(10, 10))
plt.ylim(-GRAPHSIZE,GRAPHSIZE)
plt.xlim(-GRAPHSIZE,GRAPHSIZE)
plt.axis('off')
for object in bpy.context.scene.collection.all_objects:
    print(object)
    if object.data.name == "Camera":
        continue
    allVertices = object.data.vertices
    for edge in tqdm(object.data.edges):
        eV = edge.vertices
        firstV,secondV = object.matrix_world @ (allVertices[eV[0]].co), object.matrix_world @ (allVertices[eV[1]].co)
        mag = (firstV-secondV).magnitude
        res = math.ceil( (mag/RESOLUTION))
        for i in range(res+1):
            lerped = lerpVector3(firstV,secondV,i/res)
            # plt.plot(lerped.x,lerped.y, marker="o", markersize=1,markeredgecolor="r",markerfacecolor='k')
            if lerped.z != 0:
                scaler = np.linspace(-2*lerped.z + lerped.x,2*lerped.z+lerped.x,100)
                plt.plot(scaler,calcArc(lerped.x,lerped.y,lerped.z, scaler),linewidth=RESOLUTION/3,color='k'   )
            else:
               plt.plot(lerped.x,lerped.y, marker="o", markersize=RESOLUTION/2,markeredgecolor="k",markerfacecolor='k')
# plt.figure(figsize=(10, 10))
print("saving..")               
plt.savefig("result.svg")
print("saved successfully!")
