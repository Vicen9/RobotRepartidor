class Bloque:
    Edificio = 0
    Calle_Izquierda_Derecha = 1
    Calle_Arriba_Abajo = 2
    Calle_Arriba_Derecha = 3
    Calle_Derecha_Abajo = 4
    Calle_Abajo_Izquierda = 5
    Calle_Izquierda_Arriba = 6
    Calle_Izquierda_Arriba_Derecha = 7
    Calle_Arriba_Derecha_Abajo = 8
    Calle_Derecha_Abajo_Izquierda = 9
    Calle_Abajo_Izquierda_Arriba = 10
    Calle_Arriba_Derecha_Abajo_Izquierda = 11

    #value

    def __init__(self,cod):
        self.value = cod


class Direccion:
    Arriba = 0
    Derecha = 1
    Abajo = 2
    Izquierda = 3

    #value
    def __init__(self,direccion):
        self.value = direccion


class MovGiro:
    Izquierda = 0
    Recto = 1
    Derecha = 2

    #value

    def __init__(self,MovGiro):
        self.value = MovGiro

class Casilla:

    def __init__(self, x: int, y: int, codigo_bloque: str):
        self.x = x
        self.y = y
        self.bloque = Bloque(int(codigo_bloque))


def encontrarCamino(stringMapa, posicionInicial, posicionFinal):
    def mapaMatrix(mapa):
        segmentos = [mapa[i:i + 2] for i in range(0, len(mapa), 2)]
        matriz = []
        for i in range(7):
            fila = segmentos[i * 5:(i + 1) * 5]
            matriz.append(fila)

        return matriz

    matriz = mapaMatrix(stringMapa)

    # distOptima : int = maxsize
    def matrizAdyacencia(matriz):

        def convertirMatrizCasillas(matriz):
            matCas = []
            for i in range(len(matriz)):
                fila = []
                for j in range(len(matriz[0])):
                    fila.append(Casilla(i, j, matriz[i][j]))
                matCas.append(fila)

            return matCas

        def dentroTablero(coord):
            if (coord[0] < len(matriz) and coord[0] >= 0 and coord[1] < len(matriz[0]) and coord[1] >= 0):
                return True
            return False

        matrizCasillas = convertirMatrizCasillas(matriz=matriz)

        matrizAdy = []
        for i in range(len(matriz)):
            fila = []
            for j in range(len(matriz[0])):
                fila.append(matrizCasillas[i][j].bloque.value)
            matrizAdy.append(fila)

        return matrizAdy

    matriz = matrizAdyacencia(matriz)

    #return matriz

    solOptima = []
    direcOptima = []
    sol = [posicionInicial]
    direcciones = []

    def caminoVueltraAtras(direccion, posicion):
        #global distOptima

        # print(direccion,posicion)
        # print(sol)

        def factible(direc, pos):

            def movimientoAceptado(direccion, bloque: int, bloqueSiguiente: int):

                def moviAcept(direccion, bloque: int):
                    if (direccion == Direccion.Arriba):

                        # arriba = [2,4,5,8,9,10,11]
                        arriba = [2, 3, 6, 7, 8, 10, 11]
                        if (bloque in arriba):
                            return True
                        return False
                    if (direccion == Direccion.Abajo):
                        # abajo = [2,3,6,7,8,10,11]
                        abajo = [2, 4, 5, 8, 9, 10, 11]
                        if (bloque in abajo):
                            return True
                        return False
                        # if(bloquePosterio.value == 2 or bloquePosterio.value == 3
                        #   or bloquePosterio.value == 6 or bloquePosterio.value == 7
                        #   or bloquePosterio.value == 10 or bloquePosterio.value == 11):
                        #    return True
                        # return False
                    if (direccion == Direccion.Izquierda):
                        # izquierda = [1,3,4,7,8,9,11]
                        izquierda = [1, 5, 6, 7, 9, 10, 11]
                        if (bloque in izquierda):
                            return True
                        return False
                    if (direccion == Direccion.Derecha):
                        # derecha = [1,6,7,9,10,11]
                        derecha = [1, 3, 4, 7, 8, 9, 11]
                        if (bloque in derecha):
                            return True
                        return False

                #direcSiguiente = Direccion((direccion + 2) % 4)
                direcSiguiente = (direccion + 2) % 4
                if (moviAcept(direccion, bloque) and moviAcept(direcSiguiente, bloqueSiguiente)):
                    return True
                return False

            # pos = sol[-1]
            #print(pos)
            if (pos == posicionInicial):
                #print(f"Descartado Inicio {direccion} : {pos}")
                return False

            if (pos in sol):
                #print(f"Descartado Usada {direccion} : {pos}")
                return False

            if (pos[0] < 0 or pos[0] >= len(matriz) or pos[1] < 0 or pos[1] >= len(matriz[0])):
                #print(f"Descartado Fuera de Rango {direccion} : {pos}")
                return False

            if (matriz[pos[0]][pos[1]] == 0):
                #print(f"Descartado Edificio {direccion} : {pos}")
                return False

            if (not movimientoAceptado(direc, matriz[sol[-1][0]][sol[-1][1]], matriz[pos[0]][pos[1]])):
                #print(f"Descartado Movimiento no aceptado {direccion} : {sol[-1]}")
                return False

            # if(len(sol)+1 >= distOptima):
            if (len(solOptima) > 0):
                if (len(sol) + 1 >= len(solOptima)):
                    #print(f"Descartado Muy Largo {direccion} : {pos}")
                    return False

            return True

        if (factible(direccion, posicion)):

            # print("Factible")
            sol.append(posicion)
            direcciones.append(direccion)

            pos = sol[-1]
            # bq = mAdy[pos[0]][pos[1]]
            # mAdy[pos[0]][pos[1]] = 0

            if (pos != posicionFinal):
                caminoVueltraAtras(Direccion.Arriba, (pos[0] - 1, pos[1]))
                caminoVueltraAtras(Direccion.Abajo, (pos[0] + 1, pos[1]))
                caminoVueltraAtras(Direccion.Derecha, (pos[0], pos[1] + 1))
                caminoVueltraAtras(Direccion.Izquierda, (pos[0], pos[1] - 1))
            else:
                if (len(solOptima) > 0):
                    if (len(sol) < len(solOptima)):
                        # distOptima = len(sol)
                        solOptima.clear()
                        direcOptima.clear()
                        for i in range(len(direcciones)):
                            solOptima.append(sol[i])
                            direcOptima.append(direcciones[i])
                        solOptima.append(sol[-1])
                else:
                    # distOptima = len(sol)
                    solOptima.clear()
                    direcOptima.clear()
                    for i in range(len(direcciones)):
                        solOptima.append(sol[i])
                        direcOptima.append(direcciones[i])
                    solOptima.append(sol[-1])

            # mAdy[pos[0]][pos[1]] = bq

            sol.pop()
            direcciones.pop()

    caminoVueltraAtras(Direccion.Arriba, (posicionInicial[0] - 1, posicionInicial[1]))
    caminoVueltraAtras(Direccion.Abajo, (posicionInicial[0] + 1, posicionInicial[1]))
    caminoVueltraAtras(Direccion.Derecha, (posicionInicial[0], posicionInicial[1] + 1))
    caminoVueltraAtras(Direccion.Izquierda, (posicionInicial[0], posicionInicial[1] - 1))

    # Devuelve el recogido realizado tanto en posiciones como en direcciones
    #print(solOptima,direcOptima)
    #return solOptima,direcOptima

    def arriba(posicion):
        return (posicion[0] - 1, posicion[1])

    def abajo(posicion):
        return (posicion[0] + 1, posicion[1])

    def izquierda(posicion):
        return (posicion[0], posicion[1] - 1)

    def derecha(posicion):
        return (posicion[0], posicion[1] + 1)

    def crearMov(orient: Direccion, dir):
        if (orient is dir):
            return MovGiro.Recto
        if (orient is Direccion.Derecha):
            #return MovGiro(dir)
            return dir
        if (orient is Direccion.Izquierda):
            #return MovGiro((dir + 2) % 4)
            return (dir + 2) % 4
        if (orient is Direccion.Arriba):
            #return MovGiro((dir + 1) % 4)
            return (dir + 1) % 4
        if (orient is Direccion.Abajo):
            #return MovGiro((dir - 1) % 4)
            return (dir - 1) % 4

    # print(f'Direcciones {len(direcOptima)}')
    # print(f'Casillas {solOptima}')

    pos = posicionInicial
    listaCasillas = []
    print("directOptima",direcOptima)
    orientacion = direcOptima[0]
    dirs = []

    for direc in direcOptima:

        dirs.append(crearMov(orientacion, direc))

        if (direc is Direccion.Arriba):
            listaCasillas.append(arriba(pos))
            orientacion = Direccion.Arriba

        if (direc is Direccion.Abajo):
            listaCasillas.append(abajo(pos))
            orientacion = Direccion.Abajo

        if (direc is Direccion.Izquierda):
            listaCasillas.append(izquierda(pos))
            orientacion = Direccion.Izquierda

        if (direc is Direccion.Derecha):
            listaCasillas.append(derecha(pos))
            orientacion = Direccion.Derecha
    """
    for d in dirs:
        print(d)
    print()
    solOptima.pop(0)
    """

    # for d in solOptima:
    #    print(d)
    # print()
    return dirs, solOptima
