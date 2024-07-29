#from typing import Any
import conexion as cn
import time
import ujson




class MensajeRobot:
    def __init__(self) -> None:

        print("Inicizlizando")

        def sub_cp(topic, msg):
            print("Recibido topic", topic.decode(), " mensage ", msg.decode())
            if(topic.decode() == self.topicSubs[-1]):
                self.sinc = True
            else:
                self.mensaje = str(msg.decode())


        def on_message_default(client,userdata,message):
            #print(f'Recive Topic:{message.topic} Mensage:{str(message.payload.decode("utf-8"))}')
            self.mensaje = str(message.payload.decode("utf-8"))
            if(self.mensaje.split(self.sepMsg)[0] != self.prefMsg['mapa']):
                print("EL MAPA EL MAPA EL MAPA")

        def on_message_sinc(client,userdata,message):
            #print(f'Recive Topic:{message.topic} Mensage:{str(message.payload.decode("utf-8"))}')
            self.sinc = True            

        #def on_message(client, userdata, message):    
        #    print(f'Recive Topic:{message.topic} Mensage:{str(message.payload.decode("utf-8"))}')
        #    filtrarMensage(message.topic,str(message.payload.decode("utf-8")))
            #if(message.topic == self.topicSubs[-1]):
            #        if(str(message.payload.decode("utf-8")) != str(self.__class__)):
            #            self.sinc = True
            #else:
            #    self.mensaje = str(message.payload.decode("utf-8"))

        with open("conexionConfig.json",'r') as f:
            data = ujson.load(f)

            #self.topicSubs = ["A3-467/GrupoL/Robot"]
            self.topicSubs = data['topicSubsRobot']
            #print(f'Topics a subscribir {self.topicSubs}')
            #self.topicSend = ["A3-467/GrupoL/Interfaz"]
            self.topicSend = data['topicSendRobot']
            #print(f'Topics a enviar {self.topicSend}')

            #self.prefMsg = {"mapa":'map',
            #                "pedido":'ped',
            #                "posicion":'pos'}    
            
            self.prefMsg = data['prefijoMensajes']
            self.sepMsg = data['separadorMensaje']
        
        defs = [on_message_default,on_message_sinc]
        self.conex = cn.Conexion(self.topicSubs,on_msg=sub_cp)
        self.mensaje = ""
        print("sincronizando")
        self.sinc = False
        self.__sincronizacion()
        #self.sinc = True


    def __sincronizacion(self):
        while(not self.sinc):
            self.conex.checkMensages()
            self.conex.publicar(self.topicSend[-1],self.prefMsg['sinc'])
            time.sleep(2)  
        print("SINCRONIZADO")
        self.conex.desubscribir(self.topicSubs[-1])      
        self.conex.publicar(self.topicSend[-1],self.prefMsg['sinc'])


    def getMapa(self):
        while(self.mensaje.split(self.sepMsg)[0] != self.prefMsg['mapa']):
            self.conex.checkMensages()
            time.sleep(2)

        return self.mensaje.split(self.sepMsg)[1]
    
    def getPedido(self):
        
        self.conex.publicar(self.topicSend[0],self.prefMsg['pedido'] + self.sepMsg)

        while(self.mensaje.split(self.sepMsg)[0] != self.prefMsg['pedido']):
            self.conex.checkMensages()
            #print(f"Esperando Pedido - {self.mensaje.split(self.sepMsg)[0],self.prefMsg['pedido']}")
            time.sleep(1)
        print("Pedido recibido en getPedido : ",self.mensaje.split(self.sepMsg)[1])

        ped = []
        pos = []
        i = 0
        for c in self.mensaje.split(self.sepMsg)[1]:
            pos.append(int(c))
            if( i%2 == 1):
                ped.append(pos)
                pos = []
            i = i+1

        pedi = ((ped[0][0],ped[0][1]),(ped[1][0],ped[1][1]))
        self.mensaje = ""


        return pedi
    
    def sendPosicion(self,posicion):
        self.conex.publicar(self.topicSend[0],self.prefMsg['posicion'] + self.sepMsg + str(posicion))



        
    

    



        