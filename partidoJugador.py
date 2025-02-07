import relato
import random
import time
import funciones

def generarCancha():
    """
    Crea la cancha que es una matriz de 3x3
    """
    matriz = []
    for f in range(3):
        matriz.append([])
        for _ in range(3):
            matriz[f].append(0)
    return matriz

def generarDefensores(matriz):
    """
    Coloca un defensor en cada columna de manera aleatoria
    """
    for c in range(3):
        posicionJugador = random.randint(0,2)
        matriz[posicionJugador][c] = 1

    for fila in matriz:
        print(fila)

def gambeta(direccion, matriz, posicion, enPie):
    """
    Va posicionando al jugador y chequea si sigue con la pelota
    """
    if direccion == "I" and matriz[0][posicion] != 1:
        matriz[0][posicion] = "P"
    elif direccion == "M" and matriz[1][posicion] != 1:
        matriz[1][posicion] = "P"
    elif direccion == "D" and matriz[2][posicion] != 1:
        matriz[2][posicion] = "P"
    else:
        enPie = False
    return enPie

def imprimirComentario(equipo, jugador, tipoFrase, diccionario):
    """
    Imprime un comentario aleatorio cuando hay una gambeta
    """
    randomPlayer = diccionario[equipo][jugador][random.randint(0, 2)].upper()
    relatoRandom = random.randint(0, len(tipoFrase)-1)
    print(tipoFrase[relatoRandom] + " " + randomPlayer + "...")

def imprimirMarcador(golesAFavor, golesEnContra, diccionario, miEquipo, rival):
    """
    Imprime los goles de cada equipo y sus respectivos nombres
    """
    print((diccionario[miEquipo]["nombre"] + " " + str(golesAFavor)).rjust(37), "-", str(golesEnContra), diccionario[rival]["nombre"])

def gritarGol():
    relatoRandom = random.randint(0, len(relato.frases_gol)-1)
    print(relato.frases_gol[relatoRandom])

def jugadaAtqDfc(golesAFavor, golesEnContra, diccionario, miEquipo, rival):
    """
    Arma el turno de ataque y luego el de defensa
    """
    cancha = generarCancha()
    generarDefensores(cancha)
    enPie = True
    enPieRival = True
    index = 0
    while index < 3 and enPie:
        direccion = input("Elija si quiere ir por la izquierda, derecha, o por el medio (I / D / M): ").upper()
        while direccion != "I" and direccion != "D" and direccion != "M":
            direccion = input("Dirección incorrecta (I / D / M): ").upper()
        enPie = gambeta(direccion, cancha, index, enPie)
        if enPie:
            imprimirComentario(miEquipo, "atq", relato.frases_atq, diccionario)
        else:
            imprimirComentario(rival, "dfc", relato.frases_dfc, diccionario)
        index += 1
        for fila in cancha:
            print(fila)
    print()
    if enPie:
        golesAFavor += 1
        gritarGol()
        imprimirMarcador(golesAFavor, golesEnContra, diccionario, miEquipo, rival)
    print("************************************************************************")

    index = 0
    while index < 3 and enPieRival:
        POSICIONES = ["I", "D", "M"]
        atacanteRandom = POSICIONES[random.randint(0, 2)]
        print(atacanteRandom)
        direccion = input("Elija donde colocar al defensor (I / D / M): ").upper()
        while direccion != "I" and direccion != "D" and direccion != "M":
            direccion = input("Dirección incorrecta (I / D / M): ").upper()
        enPieRival = direccion != atacanteRandom
        if enPieRival:
            imprimirComentario(rival, "atq", relato.frases_atq, diccionario)
        else:
            imprimirComentario(miEquipo, "dfc", relato.frases_dfc, diccionario)
        index += 1
    if enPieRival:
        golesEnContra += 1
        gritarGol()
        imprimirMarcador(golesAFavor, golesEnContra, diccionario, miEquipo, rival)

    return golesAFavor, golesEnContra

def actualizarDiccionario(miEquipo, rival, diccionario, golesAFavor, golesEnContra, ganador):
    """
    Actualiza el diccionario
    """
    diccionario[miEquipo]["datos"][2] += golesAFavor
    diccionario[rival]["datos"][2] += golesEnContra
    if ganador != None:
        diccionario[ganador]["datos"][1] += 3
    else:
        diccionario[miEquipo]["datos"][1] += 1
        diccionario[rival]["datos"][1] += 1

def partidoPlayer(miEquipo, rival, diccionario, tipoPartido): 
    """
    Simula todo el partido del usuario de inicio a fin
    """
    print((diccionario[miEquipo]["nombre"]+" "*5+"vs").rjust(37)+" "*5+diccionario[rival]["nombre"]+"\n")
    funciones.ejectProgressBar()
    intentos = 2
    golesAFavor = 0
    golesEnContra = 0
    ganador = None
    while intentos > 0:
        goles = jugadaAtqDfc(golesAFavor, golesEnContra, diccionario, miEquipo, rival)
        golesAFavor = 0
        golesAFavor += goles[0]
        golesEnContra = 0
        golesEnContra += goles[1]
        intentos -= 1
        print("************************************************************************")
        print()

    if golesAFavor == golesEnContra: #si hay empate y el partido es de tipo eliminatorias, se simulan penales
        if tipoPartido == "grupo":
            print()
            print("Pita el arbitro, se terminó el partido en EMPATE...")
        else:
            print("Nos vamos al TIEMPO EXTRA...")
            print()  
            intentos = 1
            while intentos > 0:
                goles = jugadaAtqDfc(golesAFavor, golesEnContra, diccionario, miEquipo, rival)
                golesAFavor = 0
                golesAFavor += goles[0] 
                golesEnContra = 0
                golesEnContra += goles[1]
                intentos -= 1
                print()
                print("************************************************************************")
                print()
                if golesAFavor == golesEnContra:
                    print("NOS VAMOS A LOS PENALES...")
                    time.sleep(1)
                    resultadoRandom1 = random.randint(0, 5)
                    resultadoRandom2 = random.randint(0, 5)
                    while resultadoRandom1 == resultadoRandom2 and abs(resultadoRandom1 - resultadoRandom2) > 3:
                        resultadoRandom1 = random.randint(0, 5)
                        resultadoRandom2 = random.randint(0, 5)
                    print()
                    if resultadoRandom1 > resultadoRandom2:
                        ganador = miEquipo
                        print(f'Señoras y señores, ha ganado {diccionario[miEquipo]["nombre"]} a {diccionario[rival]["nombre"]} por penales: {resultadoRandom1} - {resultadoRandom2}')
                        print()
                    else:
                        ganador = rival
                        print(f'Señoras y señores, ha ganado {diccionario[rival]["nombre"]} a {diccionario[miEquipo]["nombre"]} por penales: {resultadoRandom2} - {resultadoRandom1}')
                        print()
                        print("************************************************************************")
                        print()
                else:
                    print()
                    print("Pita el arbitro, se terminó el tiempo extra...")
                    print()
    else:
        if golesAFavor > golesEnContra:
            ganador = miEquipo
        else:
            ganador = rival
            print(diccionario)
        print()
        print("Pita el arbitro, se terminó el partido...")
        print()

    actualizarDiccionario(miEquipo, rival, diccionario, golesAFavor, golesEnContra, ganador)
    return golesAFavor, golesEnContra, ganador




