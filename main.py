#!/usr/bin/env pybricks-micropython
from robot import Robot

robot = Robot()
#robot.calibraSensorColor()
robot.realizaPedido()


#robot.recorreRuta(mov,cas)
#robot.recogePaquete()







"""
def sub_cp(topic, msg):
    print("Recibido topic", topic.decode(), " mensage ", msg.decode())
subs = ["A3-467/GrupoL/Robot","A3-467/GrupoL/SincRobot"]
send = ["A3-467/GrupoL/Interfaz","A3-467/GrupoL/SincInterfaz"]

import mensajeRobot as m

mR = m.MensajeRobot()
print("Creado")
print("creada conexion")
mapa = mR.getMapa()
print(mapa)

pos = (4,4)
mR.sendPosicion(pos)

"""


