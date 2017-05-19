from pyDatalog import pyDatalog
from bge import logic
import math


pyDatalog.create_terms('X,Y')
pyDatalog.create_terms('nearOb,forceTo,takeForce')
    
def takeForce(a):
    return a*3

def dlogfunc(s):
    tf = takeForce(s)
    nearOb(X) <= (X < 2)
    (forceTo[X] == tf) <= nearOb(X)
    (forceTo[X] == 0) <= ~(nearOb(X))
    return (forceTo[s] == Y).data[0]

cont = logic.getCurrentController()
scene = logic.getCurrentScene()
own = cont.owner

objList = scene.objects
obj = objList["Cube"]
objSt = objList["Cube.001"]
wPos = obj.worldPosition
wPosSt = objSt.worldPosition
daln = math.sqrt(math.pow((wPos[0] - wPosSt[0]),2) + math.pow((wPos[1] - wPosSt[1]),2) + math.pow((wPos[2] - wPosSt[2]),2))
forceY = dlogfunc(daln)[0]
local = True
force = [0.0,forceY,0.0]
obj.applyForce(force,local) 





