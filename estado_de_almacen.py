import json


def cargar_pedido(ruta_archivo):
    while(True):
        try:
            data = json.load(open(ruta_archivo))
            return data
        except:
            ruta_archivo = input("Error, introduzca la ruta de nuevo o pulse C para cancelar y volver al inicio: ")
            if ruta_archivo.upper() == "C":
                return []
                # mostrar_interfaz()
            else:
                continue



def modulos_almacen():

    data = cargar_pedido("almacen.json")

    modulos = list(data["almacen"].keys())
    print("MÓDULOS: \n \t" + str(modulos))

    return modulos


def mostrar_estado_modulo():
    data = cargar_pedido("almacen.json")
    modulos = modulos_almacen()
    modulo_ver = input("¿Qué módulo deseas ver?").upper()

    while modulo_ver not in modulos:
        modulo_ver = input('Ese módulo no existe, intentalo de nuevo').upper()
        
    print(data['almacen'][modulo_ver]['capacidad_maxima'])
    print(data['almacen'][modulo_ver]['temperatura'])
    print(data['almacen'][modulo_ver]['stock'])



# modulo = input("¿Qué módulo desea ver?")
# moleculas = estructura_molecular(modulo)
# print(moleculas)

