from bge import logic
from pyDatalog import pyDatalog

#термы
pyDatalog.create_terms('X,Y')
pyDatalog.create_terms('конецДороги,переместитьВНачало')

#функция, высчитывающая близость к концу дороги
def dlog(s):
    конецДороги(X) <= (X < -7)
    (переместитьВНачало[X] == 14.8) <= конецДороги(X)
    (переместитьВНачало[X] == s) <= ~(конецДороги(X))
    return (переместитьВНачало[s] == Y).data[0]

#определим необходимые объекты сцены и актуаторы
cont = logic.getCurrentController()
scene = logic.getCurrentScene()
own = cont.owner
act = cont.actuators["TrafficMotion"]

#задаем движение машине
act.dLoc = [0.0,-0.05,0.0]

#высчитываем координаты машины
wPos = own.worldPosition

#высчитываем, достигли ли конца дороги
moveY = dlog(wPos[1])[0]
own.worldPosition = [0.09,moveY,0.33]
