from math import pow,sqrt
from sys import maxsize


class Posicion:

        def __init__(self,x : int,y : int):
            self.x = x
            self.y = y

        def __str__(self) -> str:
            return f'({self.x},{self.y})'


class Pedido:

    def __init__(self,x_ini : int,y_ini : int, x_fin : int,y_fin : int) :
        self.inicio = Posicion(x_ini,y_ini)
        self.final = Posicion(x_fin,y_fin)

    def __str__(self) -> str:
        return f'({self.inicio},{self.final})'

    
        




def ordenarPedidos(posicionActual : Posicion,lista : list):

    def imprimir(lista : list):
        for elem in lista:
            print(elem)

    def imprimirPosiciones(lP : list):
        pos = ""
        for p in lP:
            pos = pos + str(p) + ":"
        print(pos)


    def distanciaPosicionPedido(pos: Posicion,ped : Pedido):
        return sqrt(pow(pos.x - ped.inicio.x,2) + pow(pos.y - ped.inicio.y,2))

    def distanciaPosiciones(pos1 : Posicion, pos2 : Posicion):
        return sqrt(pow(pos1.x - pos2.x,2) + pow(pos1.y - pos2.y,2))


    def transformarAPedidos(lista : list):
        listaPedidos = []
        for elem in lista:
            listaPedidos.append(Pedido(elem[0][0],elem[0][1],elem[1][0],elem[1][1]))
        return listaPedidos



    pedidos = transformarAPedidos(lista=lista)
    n_Posiciones = len(pedidos) * 2

    listaPosiciones = []
    matriz = []
    for i in range(n_Posiciones):
        m = []
        for j in range(n_Posiciones):
            m.append(maxsize)
        matriz.append(m)

    mindist = maxsize
    minPos : int
    for p in pedidos:
        posIni = len(listaPosiciones)
        listaPosiciones.append(p.inicio)
        posFin = posIni + 1
        listaPosiciones.append(p.final)
        matriz[posIni][posFin] = 0
        #matriz[posFin][posIni] = 0

        dist = distanciaPosicionPedido(pos=posicionActual,ped=p)
        #print("Posicion Actual : ",posicionActual," Pedido : ",p.inicio,p.final," Valor : ",dist)
        if(dist < mindist):
            mindist = dist
            minPos = posIni

    
    listaPedidos = [listaPosiciones[minPos]]
    
    for i in range(n_Posiciones):
        for j in range(n_Posiciones):
            # a mod 2 --> 0 : inicio , 1 : final
            if( matriz[i][j] != 0 and matriz[j][i] != 0 and i != j and i%2 == 1 and j%2 == 0):
                matriz[i][j] = distanciaPosiciones(listaPosiciones[i],listaPosiciones[j])
            
    #pos = ""
    #for p in listaPosiciones:
    #    pos = pos + str(p) + ":"
    #print(pos)
    #for m in matriz:
    #    s = ""
    #    for mj in m:
    #        if(mj != maxsize):
    #            s = f'{s}, {mj}'
    #        else:
    #            s = f'{s}, inf'
    #    print(s)

    
    while(len(listaPedidos) != n_Posiciones):
        pos = minPos
        mindist = maxsize
        minPos = -1
        for i in range(n_Posiciones):
            if(matriz[pos][i] < mindist and not listaPosiciones[i] in listaPedidos):
                mindist = matriz[pos][i]
                minPos = i
        listaPedidos.append(listaPosiciones[minPos])

    #imprimirPosiciones(listaPedidos)

    return listaPedidos

    

        
   

#posicionInicio = Posicion(6,0)

#listaPed = []
#listaPed.append(((6,4),(0,3)))
#listaPed.append(((0,1),(3,0)))

#listap = transformarAPedidos(posicionInicio,listaPed)


#peds = ordenarPedidos(posicionActual=posicionInicio,lista=listaPed)
#for p in peds:
#    print(p)
#print(transformarAPedidos(listaPed))