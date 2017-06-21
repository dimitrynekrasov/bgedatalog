from bge import logic
from pyDatalog import pyDatalog
import math

#термы
pyDatalog.create_terms('X,Y,X11,Y11,X2,Y2,X3,Y3,МРК')
pyDatalog.create_terms('изменитьСвойствоСтарт,клавишаНеНажата,клавишаНажата,начатьДвижение,изменитьСвойствоПоворот,командаСтарт,радарСработал,повернутьМРК')

#функция, определяющая нажатие клавишы
def dlogFlagSt(s):
    клавишаНеНажата(X) <= (X == False)
    (изменитьСвойствоСтарт[X] == True) <= клавишаНеНажата(X)
    (изменитьСвойствоСтарт[X] == s) <= ~(клавишаНеНажата(X))
    return (изменитьСвойствоСтарт[s] == Y).data[0]

#функция, определяющая начало движения робота по нажатой клавише
def dlogStMove(s):
    командаСтарт(X) <= (X == True)
    (начатьДвижение[X] == -0.04) <= командаСтарт(X2)
    (начатьДвижение[X] == 0.0) <= ~(командаСтарт(X2))
    return (начатьДвижение[s] == Y).data[0]

def dlogFlagPark(s,m):
    клавишаНажата(X) <= (X == True)
    (изменитьСвойствоПоворот[X,Y] == True) <= клавишаНажата(X) & радарСработал(Y)
    (изменитьСвойствоПоворот[X,Y] == False) <= ~(клавишаНажата(X) & радарСработал(Y))
    return (изменитьСвойствоПоворот[s,m] == Z).data[0]

def dlogRotSens(l,m):
    радарСработал(X) <= (X == True)
    (повернутьМРК[X,МРК] == 0.03) <= радарСработал(X) & (МРК == "Robot2")
    (повернутьМРК[X,МРК] == -0.03) <= радарСработал(X) & (МРК == "Robot1")
    (повернутьМРК[X,МРК] == 0.00) <= ~(радарСработал(X))
    return (повернутьМРК[l,m] == Y).data[0]

#определим необходимые объекты сцены, сенсоры и актуаторы
cont = logic.getCurrentController()
scene = logic.getCurrentScene()
own = cont.owner
objList = scene.objects
trafObj = objList["TrafficCar"]
act = cont.actuators["RobMotion"]
sens = cont.sensors["Forw"]
act2 = cont.actuators["MRob1"]
act3 = cont.actuators["MRob2"]

#при нажатии клавиши происходит начало движения    
own ["flagSt"] = dlogFlagSt(own ["flagSt"])[0]
act.dLoc = [0.0,dlogStMove(own ["flagSt"])[0],0.0]

#если радар видит перед собой препятствие, то робот поворачивается в необходимую сторону, чтобы выехать на дорогу
own ["passPark"] = dlogFlagPark(own["flagSt"],sens.positive)[0]
act2.dRot = [0.0,0.0,dlogRotSens(sens.positive,own.name)[0]]
        
#высчитывается близость робота к машине, которая периодически проезжает по дороге
robPos = own.worldPosition
trafPos = trafObj.worldPosition
daln = math.sqrt(math.pow((robPos[0] - trafPos[0]),2) + math.pow((robPos[1] - trafPos[1]),2) + math.pow((robPos[2] - trafPos[2]),2))

#если после поворота дальность до проезжающей машины меньше 7, то остановиться и пропускать
if ((own ["passPark"] == True) and (daln < 7)):
    act.dLoc = [0.0,0.0,0.0]
#иначе, если машины поблизости нет, то продолжать движение на проезжую часть    
else:
    act.dLoc = [0.0,-0.05,0.0]
#если робот находится в центре полосы, то запомнить это и повернуться в необходимую сторону по направлению движения    
    if ((math.fabs(robPos[0] - 0.09) < 0.01) and (own ["roadCenter"] == False)):
        own ["roadCenter"] = True
        if (own.name == "Robot2"):
            act3.dRot = [0.0,0.0,-0.7]
        elif (own.name == "Robot1"):
            act3.dRot = [0.0,0.0,0.7]

    

