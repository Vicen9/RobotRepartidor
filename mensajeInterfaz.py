#from typing import Any
import conexion2 as cn
import time
import json




class MensajeInterfaz:    


    def __init__(self) -> None:
        
        

        def on_message_default(client,userdata,message):
            print(f'Recive Topic:{message.topic} Mensage:{str(message.payload.decode("utf-8"))}')
            mensaje = str(message.payload.decode("utf-8"))
            if(mensaje.split(self.sepMsg)[0] == self.prefMsg['pedido']):
                self.pedidoSolicitado = True

            if(mensaje.split(self.sepMsg)[0] == self.prefMsg['posicion']):
                mensaje = str(message.payload.decode("utf-8"))
                sspos = mensaje.split(self.sepMsg)[1].split(",")
                ssx = int(sspos[0].split("(")[1])
                ssy = int(sspos[1].split(")")[0])
                self.posicion = (ssx,ssy)


        def on_message_mapa(client,userdata,message):
            print(f'Recive Topic:{message.topic} Mensage:{str(message.payload.decode("utf-8"))}')
            self.mapa = str(message.payload.decode("utf-8"))

            while(not self.sinc):
                time.sleep(2)

            self.__enviarMapa()
            self.conex.desubscribir(message.topic)

        def on_message_sinc(client,userdata,message):
            print(f'Recive Topic:{message.topic} Mensage:{str(message.payload.decode("utf-8"))}')
            self.sinc = True


        #def on_message(client, userdata, message):    
        #    print(f'Recive Topic:{message.topic} Mensage:{str(message.payload.decode("utf-8"))}')
        #    filtrarMensage(message.topic,str(message.payload.decode("utf-8")))

        with open(file="conexionConfig.json",mode='r') as f:
            data = json.load(f)

            #self.topicSubs = ["A3-467/GrupoL/Robot"]
            self.topicSubs = data['topicSubsInterfaz']
            print(f'Topics a subscribir {self.topicSubs}')
            #self.topicSend = ["A3-467/GrupoL/Interfaz"]
            self.topicSend = data['topicSendInterfaz']
            print(f'Topics a enviar {self.topicSend}')

            #self.prefMsg = {"mapa":'map',
            #                "pedido":'ped',
            #                "posicion":'pos'}    
            
            self.prefMsg = data['prefijoMensajes']
            self.sepMsg = data['separadorMensaje']

        defs = [on_message_default,on_message_mapa,on_message_sinc]
        self.conex = cn.Conexion(self.topicSubs,on_msg=defs)
        self.mapa = ""
        self.posicion = None
        self.pedidoSolicitado = False
        self.sinc = False
        #self.sinc = True
        self.__sincronizacion()

    def __sincronizacion(self):
        while(not self.sinc):
            self.conex.publicar(self.topicSend[-1],self.prefMsg['sinc'])
            time.sleep(2)  
        print("SINCRONIZADO")
        self.conex.desubscribir(self.topicSubs[-1])      
        self.conex.publicar(self.topicSend[-1],self.prefMsg['sinc'])

    def __enviarMapa(self):
        self.conex.publicar(self.topicSend[0],str(self.prefMsg['mapa'] + self.sepMsg + self.mapa))


    def getMapa(self):
        while(len(self.mapa) == 0):
            time.sleep(1)
        return self.mapa


    def sendPedido(self,pedido):
        msg = ""
        for pos in pedido:
            for num in pos:
                msg = msg + str(num)
        self.conex.publicar(self.topicSend[0],self.prefMsg['pedido'] + self.sepMsg + msg)
        self.pedidoSolicitado = False


    def getPosicion(self):
        print("Posicion",self.posicion)
        while(self.posicion is None):
            print("No hay posicion")
            time.sleep(1)
        return self.posicion

        
    

    

