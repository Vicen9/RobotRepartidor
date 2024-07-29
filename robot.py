from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import mensajeRobot as msg
import camino
from camino import MovGiro as mov

class Robot:
    green_rgb = (39, 74, 36)
    black_rgb = (6, 6, 13)
    tolerancia = 10
    contadorNegros = 0
    valorW = 30
    w = 0
    velocidad = 60
    velocidadNegro = 50
    negroFlag = False
    radiusCurve = 20
    interfono = None
    mapa = None
    casillaActual = (6,4)
    pedido = None
    casillaSig = None

    def __init__(self):
        self.ev3 = EV3Brick()
        left_motor = Motor(Port.A)
        right_motor = Motor(Port.D)
        self.pala = Motor(Port.B)
        self.giroSensor = GyroSensor(Port.S1)
        self.colorSensor = ColorSensor(Port.S4)
        self.robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=124)
        self.robot.settings(straight_speed=self.velocidad)
        self.interfono = msg.MensajeRobot()
        self.mapa = self.interfono.getMapa()
        self.interfono.sendPosicion(self.casillaActual)


    #Metodos gestion negros
    def queNegroEs(self,negro):
        if negro == 0:
            return 0
        if negro % 2 == 0:
            return 0
        return 1

    def resetContadorNegros(self):
        self.contadorNegros = 0

    def incrementaContNegros(self):
        self.contadorNegros = self.contadorNegros + 1

    #metodos deteccion de colores
    def is_green(self,rgb):
        if (rgb[0] >= (Robot.green_rgb[0]-Robot.tolerancia) and rgb[0] <= (Robot.green_rgb[0]+Robot.tolerancia)) and (rgb[1] >= (Robot.green_rgb[1]-Robot.tolerancia) and rgb[1] <= (Robot.green_rgb[1]+Robot.tolerancia)) and (rgb[2] >= (Robot.green_rgb[2]-Robot.tolerancia) and rgb[2] <= (Robot.green_rgb[2]+Robot.tolerancia)):
            return True
        return False

    def is_black(self,rgb):
        if (rgb[0] >= (Robot.black_rgb[0]-Robot.tolerancia) and rgb[0] <= (Robot.black_rgb[0]+Robot.tolerancia)) and (rgb[1] >= (Robot.black_rgb[1]-Robot.tolerancia) and rgb[1] <= (Robot.black_rgb[1]+Robot.tolerancia)) and (rgb[2] >= (Robot.black_rgb[2]-Robot.tolerancia) and rgb[2] <= (Robot.black_rgb[2]+Robot.tolerancia)):
            return True
        return False

    def calibraSensorColor(self):
        while True:
            print(self.colorSensor.rgb())
            wait(20)

    #Metodos para el movimiento
    def giro(self,grados):
        self.giroSensor.reset_angle(0)
        self.robot.turn(grados)
        while (self.giroSensor.angle() != grados):
            diferencia = self.giroSensor.angle() - grados
            ajuste = diferencia * -1
            for i in range(abs(ajuste)):
                if (ajuste > 0):
                    self.robot.turn(1)
                elif (ajuste < 0):
                    self.robot.turn(-1)

    def giraDerecha(self):
        self.robot.straight(62) #60
        self.giro(90)
        self.sigueRecto()

    def giraIzquierda(self):
        self.robot.straight(62) #60
        self.giro(-90)
        self.sigueRecto()

    def mediaVuelta(self):
        self.robot.straight(70)
        self.giro(90)
        self.giro(90)
        self.giro(-10)

    def sigueRecto(self, color=green_rgb):
        # Valores iniciales
        rgb = self.colorSensor.rgb()
        negroAnteriorFlag = self.negroFlag
        contNegroAnterior = self.contadorNegros
        if self.is_black(rgb):
            self.negroFlag = True
        while (((self.queNegroEs(contNegroAnterior) == 1) and (self.queNegroEs(self.contadorNegros) == 0)) == False) or self.contadorNegros == 0:

            #Fase de lectura
            rgb = self.colorSensor.rgb()

            #Fase de control
            if self.is_green(rgb):
                self.w = self.valorW
                self.velocidad = Robot.velocidad
                negroAnteriorFlag= self.negroFlag
                self.negroFlag = False

            elif self.is_black(rgb):
                negroAnteriorFlag = self.negroFlag
                self.negroFlag = True
                self.w = 0
                self.velocidad = self.velocidadNegro

            else:
                negroAnteriorFlag= self.negroFlag
                self.negroFlag = False
                self.w = -self.valorW
                self.velocidad = Robot.velocidad

            #Fase de ejecución
            #Incremento negro al entrar
            if not negroAnteriorFlag and self.negroFlag:
                contNegroAnterior = self.contadorNegros
                self.incrementaContNegros()
                # Actualizacion de casilla
                #if self.queNegroEs(self.contadorNegros) == 1:
                    #self.actualizaCasilla()

            #Pendiente comprobar si hilo va a su bola o se para
            self.robot.drive(self.velocidad,self.w)

            #print(self.contadorNegros)

    def recogePaquete(self):
        self.robot.stop()
        self.pala.run_target(70,-60)


    def soltarPaquete(self):
        self.robot.stop()
        self.pala.run_target(70,0)


    #Deficnición y realización de la ruta
    # Recogemos la lista de movimientos del algoritmo
    def recogePedido(self):
        self.pedido = self.interfono.getPedido()
        return True

    def actualizaCasilla(self):
        self.casillaActual = self.casillaSig
        self.interfono.sendPosicion(self.casillaSig)

    def recorreRuta(self,rutaDirecciones,rutaCoordenadas):
        for dir,coor in zip(rutaDirecciones,rutaCoordenadas):
            self.casillaSig = coor
            self.actualizaCasilla()
            if dir is 2:
                self.giraDerecha()
            elif dir is 0:
                self.giraIzquierda()
            else:
                self.sigueRecto()


    def realizaPedido(self):
        while self.recogePedido():
            #posicion actual ---> A
            print("Recogida Principio",self.casillaActual," Final ",self.pedido[0])
            rutaDirecciones,rutaCoordenadas = camino.encontrarCamino(self.mapa,self.casillaActual,self.pedido[0])
            print("Pedido Recogida:",rutaDirecciones,rutaCoordenadas)
            self.recorreRuta(rutaDirecciones,rutaCoordenadas)
            self.recogePaquete()
            self.mediaVuelta()
            self.casillaSig = rutaCoordenadas[-1]
            self.actualizaCasilla()

            #Ir desde punto A ---> B
            print("Entrega Principio",self.pedido[0]," Final ",self.pedido[1])
            rutaDirecciones,rutaCoordenadas = camino.encontrarCamino(self.mapa,self.pedido[0],self.pedido[1])
            print("Pedido Soltar:",rutaDirecciones,rutaCoordenadas)
            self.recorreRuta(rutaDirecciones, rutaCoordenadas)
            self.soltarPaquete()
            self.mediaVuelta()
            self.casillaSig = rutaCoordenadas[-1]
            self.actualizaCasilla()
            self.robot.stop()
