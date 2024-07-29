#import paho.mqtt.client as mqtt
import ujson
from umqtt.robust import MQTTClient

class Conexion:   


    def __init__(self, topics:list,on_msg):

        
        with open("conexionConfig.json",'r') as f:
            data = ujson.load(f)
            self.__broker_address = data['ipbroker']
            self.__port = int(data['portbroker'])

            # Configuración del broker MQTT
            #self.__broker_address = "192.168.48.245"  # Cambia por la dirección de tu broker MQTT
            #self.__broker_address = "192.168.0.100"  # Cambia por la dirección de tu broker MQTT
            #self.__port = 1883  # Puerto predeterminado para MQTT
        #self.__topic = ["A3-467/GrupoL","map"]
        self.__topic = topics

        

        #def on_message(client, userdata, message):
        #    print("message received " ,str(message.payload.decode("utf-8")))
        #    print("message topic=",message.topic)
        #    print("message qos=",message.qos)
        #    print("message retain flag=",message.retain)
        #    #self.__listaPendientes.append(f'{message.topic}-{message.payload.decode("utf-8")}')
        ########################################
        #broker_address="192.168.0.19"
        #broker_address="iot.eclipse.org"
        print("creating new instance")
        #self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client = MQTTClient("RobotPACO",self.__broker_address)
        self.client.set_callback(on_msg)
        self.client.connect()
        #client.on_message = on_message
        #client.on_message=on_message #attach function to callback
        #client.on_message = on_msg

        """
        for tp,df in zip(topics,on_msg):
            self.client.message_callback_add(tp,df)
            print(f" Funcion {df} adjunta a {tp}")
        
        print("connecting to broker")
        self.client.connect(self.__broker_address,self.__port) #connect to broker
        """
        for tp in topics:
            self.client.subscribe(tp)
            print("Subscrito a ",tp)
            #print(f" Subscrito a {tp}")

        #self.__client = self.__connect_mqtt()
        #self.inicializar()
        #self.__client.loop_start()
        #self.client.loop_start() #start the loop


        #self.subscribe(cliente=client,topic=self.__topic)
        print("Inicializado")

        #self.__listaPendientes = listaPendientes
        #self.__client.loop_forever()

        

    def publicar(self,topic,msg):
        
        #client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)        
        #client.connect(self.__broker_address, self.__port)
        print("Enviar  a topic",topic," mensage ",msg)
        self.client.publish(topic,msg)
        #client.disconnect()
        #result = self.__client.publish(self.__topic[0],msg)
        # result: [0, 1]

    def desconectar(self):
        self.client.loop_stop()
        self.client.disconnect()
        print("Desconectado")

    def desubscribir(self,topic):
        #self.client.unsubscribe(topic)
        print("Desubscrito topic : ",topic)

    def checkMensages(self):
        self.client.check_msg()


# Función para enviar mensajes MQTT al broker

def publicarOut( topic, msg):
    # client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    # client.connect(self.__broker_address, self.__port)
    print("Enviar  a topic", topic, " mensage ", msg)
    client = MQTTClient("PACO", "192.168.48.245")
    client.connect()
    client.publish(topic, msg)
"""
def send_mqtt_message( topic,message):
    client = MQTTClient("PACO",)
    client.connect("192.168.0.19" , 1883)
    client.publish(topic, message)
    client.disconnect()

#    def publish(client):
#        msg_count = 1
#        while True:
#            #time.sleep(1)
#            msg = f"messages: {msg_count}"
#            result = client.publish(topic, msg)
#            # result: [0, 1]
#            status = result[0]
#            if status == 0:
#                print(f"Send `{msg}` to topic `{topic}`")
#            else:
#                print(f"Failed to send message to topic {topic}")
#            msg_count += 1
#            if msg_count > 5:
#                break


    #def __subscribe(client: mqtt, topic):

    #def run():
    #    client = connect_mqtt()
    #    client.loop_start()
    #    publish(client)
    #    client.loop_stop()

    #def run():
    #    client = connect_mqtt()
    #    subscribe(client)
    #    client.loop_forever()
    
"""
