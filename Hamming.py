import random


class Hamming:
    def __init__(self, tamanio=0, cadena=None, es_error=False):
        self.hamming_error = None
        self.es_error = es_error
        if cadena is None:
            self.cadena = self.generar_cadena(tamanio)
        else:
            self.cadena = cadena
        self.matriz = self.generar_matriz()
        self.hamming()

    def generar_cadena(self, tamanio):
        cadena = ""
        for i in range(tamanio):
            cadena += str(random.randint(0, 1))
        return cadena

    def generar_matriz(self):
        matriz = [[], []]
        cont = 0
        num_potencias = 0
        for i in range(1, 2 ** len(self.cadena)):
            if self.esPotenciaDe2(i):
                matriz[1].append("")
                num_potencias += 1
            elif len(self.cadena) > cont:
                matriz[1].append(self.cadena[cont])
                cont += 1
            else:
                break
        for i in range(len(matriz[1])):
            matriz[0].append(bin(i+1)[2:])
        matriz = self.completa_ceros(matriz)
        for i in range(num_potencias):
            matriz.append([])
        matriz.append([])
        return matriz

    def esPotenciaDe2(self, numero):
        return (numero != 0) and (numero & (numero - 1) == 0)

    def get_cadena(self):
        return self.cadena

    def set_cadena(self, cadena):
        self.cadena = cadena

    def get_matriz(self):
        return self.matriz

    def set_matriz(self, matriz):
        self.matriz = matriz

    def completa_ceros(self, matriz):
        num_ceros = len(matriz[0][len(matriz[0])-1])
        for i in range(len(matriz[0])):
            for j in range(len(matriz[0][i]), num_ceros):
                matriz[0][i] = "0" + matriz[0][i]
        return matriz

    def completa(self, fila_actual, potencia_actual):
        num_ceros = 0
        num_unos = 0
        for i in range(len(self.matriz[fila_actual])):
            if self.matriz[fila_actual][i] == "1":
                num_unos += 1
            elif self.matriz[fila_actual][i] == "0":
                num_ceros += 1
        if num_unos % 2 == 0:
            self.matriz[fila_actual][2 ** potencia_actual - 1] = "0"
        else:
            self.matriz[fila_actual][2 ** potencia_actual - 1] = "1"

    def paridad(self):
        self.paridad_rec(2, -1, 0)

    def paridad_rec(self, fila_actual, caracter_actual, potencia_actual):
        if fila_actual == len(self.matriz)-1:
            return
        for i in range(len(self.matriz[fila_actual-1])):
            if not self.esPotenciaDe2(i+1) and self.matriz[0][i][caracter_actual] == '1':
                self.matriz[fila_actual].append(self.matriz[1][i])
            else:
                self.matriz[fila_actual].append("")
        self.completa(fila_actual, potencia_actual)
        self.paridad_rec(fila_actual+1, caracter_actual-1, potencia_actual + 1)

    def baja_datos(self):
        for j in range(len(self.matriz[0])):
            for i in range(1, len(self.matriz)-1):
                if self.matriz[i][j] != "":
                    self.matriz[-1].append(self.matriz[i][j])
                    break

    def genera_error_aleatorio(self):
        rand = random.randint(1, len(self.matriz[-1])-1)
        if self.esPotenciaDe2(rand):
            return self.genera_error_aleatorio()
        return rand-1

    def obtener_digitos(self, cadena):
        cadena_error = ""
        for i in range(len(cadena)):
            if not self.esPotenciaDe2(i+1):
                cadena_error += cadena[i]
        return cadena_error

    def comparar_paridades(self, cadena_original, cadena_error):
        co_aux = ""
        ce_aux = ""
        verifica = ""
        for i in range(len(cadena_original)):
            if self.esPotenciaDe2(i+1):
                if cadena_original[i] == cadena_error[i]:
                    verifica += "0"
                else:
                    verifica += "1"
                co_aux += cadena_original[i]
                ce_aux += cadena_error[i]
        print("Paridades de la original:", co_aux)
        print("Paridades con error:", ce_aux)
        print("El verifica quedo:", verifica)
        verifica = verifica[::-1]
        print("Le aplicamos la reversa:", verifica)
        verifica = int(verifica, 2)
        print("Por lo tanto, el error esta en el bit:", verifica)
        return verifica-1

    def hamming(self):
        print("Ejecutando hamming...")
        print("La cadena generada es:", self.cadena)
        self.paridad()
        self.baja_datos()
        print("La matriz generada es:")
        for i in range(len(self.matriz)):
            print(self.matriz[i])
        cadena_a_transmitir = "".join(self.matriz[-1])
        print("La cadena a transmitir es:", cadena_a_transmitir)
        if not self.es_error:
            print("Generando error aleatorio...")
            error = self.genera_error_aleatorio()
            if cadena_a_transmitir[error] == "0":
                cadena_error = cadena_a_transmitir[:error] + \
                    "1" + cadena_a_transmitir[error+1:]
            else:
                cadena_error = cadena_a_transmitir[:error] + \
                    "0" + cadena_a_transmitir[error+1:]
            print("La cadena con el error es:", cadena_error)
            print("Procesando error...")
            cadena_error_digitos = self.obtener_digitos(cadena_error)
            aux = Hamming(cadena=cadena_error_digitos, es_error=True)
            print("Comparando paridades...")
            verifica = self.comparar_paridades(
                cadena_a_transmitir, "".join(aux.get_matriz()[-1]))
            print("Cadena original:", cadena_a_transmitir)
            print("Cadena con error:", cadena_error)
            print("Corregimos el error...")
            cadena_error = list(cadena_error)
            if cadena_error[verifica] == "0":
                cadena_error[verifica] = "1"
            else:
                cadena_error[verifica] = "0"
            cadena_error = "".join(cadena_error)
            print("Cadena original:", cadena_a_transmitir)
            print("Cadena corregida:", cadena_error)


if __name__ == "__main__":
    print("Bienvenid@")
    while True:
        print("¿Deseas generar una cadena aleatoriamente?")
        print("1. Si")
        print("2. No, yo deseo escribirla")
        print("3. Salir")
        decision = int(input("Ingresa tu opción: "))
        if decision == 1:
            print("¿De cuantos bits?")
            tamanio = int(input("Ingresa los bits: "))
            h = Hamming(tamanio=tamanio)
        elif decision == 2:
            print("Recuerda que solo debes ingresar 1 y 0")
            cadena = input("Ingresa la cadena: ")
            for i in cadena:
                if i != "0" and i != "1":
                    print("Pusiste un caracter invalido")
                    exit(-1)
            h = Hamming(cadena=cadena)
        else:
            print("Adios!! Te esperamos pronto")
            exit(0)
