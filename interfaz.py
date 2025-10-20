import PEDIDOS_CONJUNTO 
import estado_de_almacen
import demanda

def interfaz_iniciar():    

    while True:

            print("---------------  Menú principal  ------------------\n")
            print("1 - Información general del programa.")
            print("2 - Estado del almacén.")
            print("3 - Pedidos.")
            print("4 - Análisis datos históricos.")
            print("5 - Salir del programa.\n")
            print("---------------  Menú principal  ------------------")
            
            opcion = input("Selecciona una opción: ")

            if opcion == "2":

                print("\n---------------  Menú de estado del almacén  ------------------\n")
                print("1  Mostrar los módulos del almacén.")
                print("2  Mostrar el estado de un módulo.")
                print("B  Vuelve al menú anterior\n.")

                opcion_2 = input('Selecciona una opción').upper()
                opcion_2_opciones = ['1','2','B']

                while opcion_2 not in opcion_2_opciones:
                     opcion_2 = input('SELECCIONA UNA DE LAS OPCIONES POR FAVOR: ').upper()


                if opcion_2 == '1': 
                     estado_de_almacen.modulos_almacen()
                elif opcion_2 == '2':
                     estado_de_almacen.mostrar_estado_modulo()
                elif opcion_2 == 'B':                                   
                    continue
                         

                

            elif opcion == "3":


                print("---------------  Menú de gestión de pedidos  ------------------\n")
                print("1  Mostrar los pedidos sin procesar..")
                print("2  Procesar pedido.")
                print("3  Mostrar los pedidos en marcha.")
                print("B  Vuelve al menú anterior.\n")
                print("---------------  Menú de gestión de pedidos  ------------------")

                opcion_3 = input('Selecciona una opción')
                opcion_3_opciones = ['1','2','3','B']
                while opcion_3 not in opcion_3_opciones:
                     opcion_3 = input('SELECCIONA UNA DE LAS OPCIONES POR FAVOR: ')



                if opcion_3 == '1': 
                    print(PEDIDOS_CONJUNTO.pedidos_sin_procesar())
                elif opcion_3 == '2':
                    print(PEDIDOS_CONJUNTO.pedidos_sin_procesar())
                    pedido_procesar = input('Introduzca pedido a procesar: ').upper()

                    while pedido_procesar not in PEDIDOS_CONJUNTO.pedidos_sin_procesar():
                          pedido_procesar = input('Error, pedido no encontrado, introduzca pedido de nuevo:').upper()

                    PEDIDOS_CONJUNTO.procesar_pedido(pedido_procesar)
                    print(f'Pedido {pedido_procesar} procesado.')

                elif opcion_3 == '3':
                    PEDIDOS_CONJUNTO.ver_pedidos_en_marcha()
                    continue                             

            elif opcion == "4":


                print("---------------  Menú de datos históricos  ------------------\n")
                print("1  Contador de pedidos.")
                print("2 Volumen de unidades por producto")
                print("3 Evolución temporal de unidades")  # 3 y 4
                print("4 Análisis de estacionalidad")
                print("5 Análisis de pedidos por zona")
                print("6 Datos demográficos")
                print("7 Estacionalidad de enfermedades")
                print("8 Integración con marcadores epidemiológicos")
                print("B Vuelve al menú anterior \n")
                print("---------------  Menú de datos históricos  ------------------")

                opcion_4 = input('Selecciona una opción')
                opcion_4_opciones = ['1','2','3','4','5','6','7','8','B']
                while opcion_4 not in opcion_4_opciones:
                     opcion_4 = input('SELECCIONA UNA DE LAS OPCIONES POR FAVOR: ')



                if opcion_4 == '1': 
                    poraño = input('¿Quiere ver el número de pedidos agrupado por año? Y/N').upper()
                    if poraño == 'Y':
                         poraño = True
                         pedidos,clientes,incidencia = demanda.cargar_datos("pedidos-2.csv","clientes.csv","incidencia.csv")
                         demanda.contar_pedidos(pedidos,poraño)
                    else:
                        pedidos,clientes,incidencia = demanda.cargar_datos("pedidos-2.csv","clientes.csv","incidencia.csv")
                        demanda.contar_pedidos(pedidos)


                elif opcion_4 == '2':
                    pedidos, clientes, incidencia = demanda.cargar_datos("pedidos-2.csv", "clientes.csv", "incidencia.csv")
                    entrada = input('¿Qué años te gustaría filtrar? (Ingrese los años separados por coma, o deje en blanco para no filtrar): ')
                    if entrada.strip() == '':
                        años = None
                    else:
                        años = []
                        for año in entrada.split(','):
                            año = año.strip()  # Eliminar espacios innecesarios
                            años.append(int(año))  # Convertir a entero y añadir a la lista
                    top_n_input = int(input('¿Cuántos productos quiere ver? (Ingrese 0 para ver todos, o un número específico para limitar): '))
                
                    plot = input('¿Desea ver el gráfico de barras? (Y/N): ').strip().upper()

                    if plot == 'Y':
                        plot = True
                    elif plot == 'N':
                        plot = False
                    else:
                        print("Opción no válida, no se mostrará el gráfico.")
                        plot = False
                    resultado = demanda.unidades_por_producto(pedidos, top_n=top_n_input, años=años, plot=plot)
                    print(resultado)

                elif opcion_4 == '3':
                    print("---------------  Evolución temporal de unidades  ------------------")
                    print("1 - Evolución mensual de un producto.")
                    print("2 - Comparar productos.")


                    opciones_grupo_4 = input("Selecciona una opción: ").strip()

                    if opciones_grupo_4 == '1':
                        demanda.mostrar_codigos_productos()
                        pedidos, clientes, incidencia = demanda.cargar_datos("pedidos-2.csv", "clientes.csv", "incidencia.csv")
                        codigo_producto = input('Introduce el código del producto para analizar su evolución mensual: ').strip().upper()

                        plot = input('¿Desea ver el gráfico de evolución mensual? (Y/N): ').upper()
                        if plot == 'Y':
                            plot = True
                        elif plot == 'N':
                            plot = False
                        else:
                            print("Opción no válida, no se mostrará el gráfico.")
                            plot = False

                        resultado = demanda.evolucion_producto(pedidos, codigo_producto, plot)


                        print("\nEvolución mensual del producto:")
                        print(resultado)

                    elif opciones_grupo_4 == '2':
                        demanda.mostrar_codigos_productos()
                        pedidos, clientes, incidencia = demanda.cargar_datos("pedidos-2.csv", "clientes.csv", "incidencia.csv")
                        codigos_input = input('Introduce los códigos de los productos para comparar, separados por coma: ').strip().upper()

                        codigos = []
                        for codigo in codigos_input.split(','):
                            codigo = codigo.strip()
                            codigos.append(codigo)
                        plot = input('¿Desea ver el gráfico de comparación? (Y/N): ').upper()
                        if plot == 'Y':
                            plot = True
                        elif plot == 'N':
                            plot = False
                        else:
                            print("Opción no válida, no se mostrará el gráfico.")
                            plot = False

                        resultado = demanda.comparar(pedidos, codigos, plot)
                        print("\nComparación de productos:")
                        print(resultado)

                elif opcion_4 == '4':
                    demanda.mostrar_codigos_productos()
                    pedidos, clientes, incidencia = demanda.cargar_datos("pedidos-2.csv", "clientes.csv", "incidencia.csv")
                    codigo_producto = input('Introduce el código del producto para analizar su estacionalidad: ').strip().upper()

                    plot = input('¿Desea ver el gráfico de estacionalidad? (Y/N): ').upper()
                    if plot == 'Y':
                        plot = True
                    elif plot == 'N':
                        plot = False
                    else:
                        print("Opción no válida, no se mostrará el gráfico.")
                        plot = False
                    resultado = demanda.estacionalidad_productos(pedidos, codigo_producto, plot)
                    print(resultado)
                
                elif opcion_4 == '5':
                    pedidos, clientes, incidencia = demanda.cargar_datos("pedidos-2.csv", "clientes.csv", "incidencia.csv")
                    agrupacion = demanda.pedidos_por_zona(pedidos,clientes)
                    print(agrupacion)

                elif opcion_4 == '6':
                    demanda.mostrar_codigos_productos()
                    pedidos, clientes, incidencia = demanda.cargar_datos("pedidos-2.csv", "clientes.csv", "incidencia.csv")
                    farmacos = input('Introduce los códigos de los productos para comparar, separados por coma: ').strip().upper()

                    lista_farmacos = []
                    for farmaco in farmacos.split(','):
                        farmaco = farmaco.strip()
                        lista_farmacos.append(farmaco)
                    if lista_farmacos == '':
                        lista_farmacos = None
                    agrupacion = demanda.demanda_vs_poblacion(pedidos,clientes,lista_farmacos)
                    print(agrupacion)

                elif opcion_4 == '7':
                    pedidos, clientes, incidencia = demanda.cargar_datos("pedidos-2.csv", "clientes.csv", "incidencia.csv")
                    plot = input('¿Desea ver el gráfico de estacionalidad? (Y/N): ').upper()
                    if plot == 'Y':
                        plot = True
                    elif plot == 'N':
                        plot = False
                    else:
                        print("Opción no válida, no se mostrará el gráfico.")
                        plot = False
                    
                    agrupacion = demanda.estacionalidad_enfermedad(incidencia,plot)
                    print(agrupacion)

                
                elif opcion_4 == '8':
                    pedidos, clientes, incidencia = demanda.cargar_datos("pedidos-2.csv", "clientes.csv", "incidencia.csv")
                    plot = input('¿Desea ver el gráfico de estacionalidad? (Y/N): ').upper()
                    if plot == 'Y':
                        plot = True
                    elif plot == 'N':
                        plot = False
                    else:
                        print("Opción no válida, no se mostrará el gráfico.")
                        plot = False
                    codigos_validos = demanda.mostrar_codigos_productos()
                    codigo_producto = input('Introduce el código del producto para analizar su demanda con respecto a alguna enfermedad: \n').strip().upper()
                    while codigo_producto not in codigos_validos:
                        codigo_producto = input('Introduce el código del producto para analizar su demanda con respecto a alguna enfermedad: \n').strip().upper()


                    enfermedades_validas = demanda.enfermedades()
                    enfermedad = input('Introduce una enfermedad para analizarla con respecto al fármaco selecionado: ').strip()
                    while enfermedad not in enfermedades_validas:
                        print(f'Las enfermedades válidas son: \n{enfermedades_validas}')
                        enfermedad = input('Introduce una enfermedad para analizarla con respecto al fármaco selecionado: ').strip()

                    agrupacion = demanda.pedidos_vs_incidencia(pedidos, incidencia, codigo_producto, enfermedad, plot)
                    print(agrupacion)

                elif opcion_4 == 'B':
                    continue 
            elif opcion == "5":
                break



interfaz_iniciar()