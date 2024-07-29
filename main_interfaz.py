import mensajeInterfaz as msg
import time

msgInterfaz = msg.MensajeInterfaz()

mapa = msgInterfaz.getMapa()
print(f"Mapa recibido {mapa}")

print("Comprobando solicitud")
while(not msgInterfaz.pedidoSolicitado):
    time.sleep(1)
    print("Comprobando solicitud")

posicion = msgInterfaz.getPosicion()
print(f"Posicion Recibida {posicion}")
print(f'Posicion x = {posicion[0]} : y = {posicion[1]}')

pedido = ((4,5),(7,9))
msgInterfaz.sendPedido(pedido)
print("Pedido enviado")

time.sleep(60)