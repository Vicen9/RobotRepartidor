import conexion2 as cn
import time

mapa = "0202000105030705000200041109060110031000000200080101100110000106010701"

while(True):
    
    
    cn.send_mqtt_message("map",mapa)
    print("Enviado")
    time.sleep(20)
    
    """
    topic = "A3-467/GrupoL/Interfaz"
    msg = "pos:(6,1)"
    cn.send_mqtt_message(topic, msg)
    time.sleep(10)
    msg = "pos:(5,1)"
    cn.send_mqtt_message(topic, msg)
    time.sleep(10)
    msg = "pos:(4,1)"
    cn.send_mqtt_message(topic, msg)
    time.sleep(10)
    msg = "pos:(3,1)"
    cn.send_mqtt_message(topic, msg)
    time.sleep(10)
    """