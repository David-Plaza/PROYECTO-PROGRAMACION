import PEDIDOS_CONJUNTO 
import estado_de_almacen


def interfaz_iniciar():    



    while True:

            print("---------------  Menú principal  ------------------\n")
            print("1 - Estado del Almacén.")
            print("2 - Pedidos.")
            print("3 - Informes históricos.")
            print("4 - Salir del programa.\n")
            print("---------------  Menú principal  ------------------")
            
            opcion = input("Selecciona una opción: ")

            if opcion == "1":

                print("\n---------------  Menú de estado del almacén  ------------------\n")
                print("1 – Mostrar los módulos del almacén.")
                print("2 – Mostrar el estado de un módulo.")
                print("B – Vuelve al menú anterior\n.")

                opcion_1 = input('Selecciona una opción').upper()
                opcion_1_opciones = ['1','2','B']

                while opcion_1 not in opcion_1_opciones:
                     opcion_1 = input('SELECCIONA UNA DE LAS OPCIONES POR FAVOR: ').upper()


                if opcion_1 == '1': 
                     estado_de_almacen.modulos_almacen()
                elif opcion_1 == '2':
                     estado_de_almacen.mostrar_estado_modulo()
                elif opcion_1 == 'B':                                   
                    continue
                         

                

            elif opcion == "2":

                print("1 - Menú de los pedidos.")
                print("---------------  Menú de pedidos  ------------------\n")
                print("1 – Mostrar los pedidos sin procesar..")
                print("2 – Procesar pedido.")
                print("3 – Mostrar los pedidos en marcha.")
                print("B – Vuelve al menú anterior.\n")
                print("---------------  Menú de pedidos  ------------------")

                opcion_2 = input('Selecciona una opción')
                opcion_2_opciones = ['1','2','3','B']
                while opcion_2 not in opcion_2_opciones:
                     opcion_2 = input('SELECCIONA UNA DE LAS OPCIONES POR FAVOR: ')



                if opcion_2 == '1': 
                    print(PEDIDOS_CONJUNTO.pedidos_sin_procesar())
                elif opcion_2 == '2':
                    print(PEDIDOS_CONJUNTO.pedidos_sin_procesar())
                    pedido_procesar = input('Introduzca pedido a procesar: ').upper()

                    while pedido_procesar not in PEDIDOS_CONJUNTO.pedidos_sin_procesar():
                          pedido_procesar = input('Error, pedido no encontrado, introduzca pedido de nuevo:').upper()

                    PEDIDOS_CONJUNTO.procesar_pedido(pedido_procesar)
                    print(f'Pedido {pedido_procesar} procesado.')

                elif opcion_2 == '3':
                    PEDIDOS_CONJUNTO.ver_pedidos_en_marcha()
                    continue                             


