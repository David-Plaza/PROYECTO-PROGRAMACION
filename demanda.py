import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def convertir_fecha(df):
    #Convertimos la columna fecha tipo datetime y añadimos columnas de año, mes, y primer día del mes
    df = df.copy()
    df['fecha'] = pd.to_datetime(df['fecha'], errors="coerce")
    df["año"] = df['fecha'].dt.year
    df["mes"] = df['fecha'].dt.month
    df["fecha_mes"] = df['fecha'].dt.to_period("M").dt.to_timestamp()
    # print(df)
    return df

#TEST:
# df = pd.read_csv("pedidos-2.csv")  
# convertir_fecha(df)

def cargar_datos(ruta_pedidos, ruta_clientes, ruta_incidencia):
    #Cargamos los csv
    pedidos = pd.read_csv(ruta_pedidos)
    clientes = pd.read_csv(ruta_clientes)
    incidencia = pd.read_csv(ruta_incidencia)

    pedidos = convertir_fecha(pedidos)
    incidencia = convertir_fecha(incidencia)
    return pedidos, clientes, incidencia

# TEST: 
# pedidos, clientes, incidencia = cargar_datos("pedidos-2.csv","clientes.csv","incidencia.csv")

def contar_pedidos(df_pedidos, por_anyo=False):
    if por_anyo:
        tabla = (df_pedidos.dropna(subset=["pedido_id", "fecha"]).groupby("año")["pedido_id"].nunique().reset_index(name="pedidos_totales").sort_values("año"))
        print(tabla)
        return tabla
    else:
        total = df_pedidos["pedido_id"].nunique()
        print(f"Total de pedidos únicos: {total}")
        return total
    
#TEST: 
# df = pd.read_csv("pedidos-2.csv") 
# df = convertir_fecha(df)
# contar_pedidos(df)
# contar_pedidos(df,  por_anyo=True)

def unidades_por_producto(df_pedidos,top_n=-1, años = None, plot = False):
    df = df_pedidos.copy()

    # Filtra por años si se indica en el input de la función
    if años is not None:
        df = df[df["año"].isin(años)]

    # Agrupamos por producto id y nombre del producto
    tabla = (df.groupby(["producto_id", "nombre_producto"], as_index=False)["unidades"].sum().sort_values("unidades", ascending=False))

    # Ponemos la condicion de que top_n sea numero entero y que sea mayor que 0, si es así, entonces devolvemoss la tabla con los primeros top_n valores
    if isinstance(top_n, int) and top_n > 0:
        tabla = tabla.head(top_n)
    
    # Solo en el caso de que se especifique que plot = True como input, se muestra el gráfico de barras
    if plot == True:
        
        plt.figure()
        plt.bar(tabla["nombre_producto"], tabla["unidades"])
        plt.title("Unidades por producto")
        plt.xlabel("Producto")
        plt.ylabel("Unidades")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.show()

    return tabla.reset_index(drop=True)

df = pd.read_csv("pedidos-2.csv")
df = convertir_fecha(df)

#TEST:
# print(unidades_por_producto(df))
# print(unidades_por_producto(df, top_n=2)) #por ejemplo, compropbamos los 2 productos más vendidos
# print(unidades_por_producto(df, años=[2023, 2024, 2025])) 
# print(unidades_por_producto(df, top_n=5, años=[2025], plot=True))

def evolucion_producto(df_pedidos, codigo_producto, plot = False):
    df = df_pedidos.copy()
    df = df[df["producto_id"] == codigo_producto]

    nuevo_df = (df.groupby("fecha_mes", as_index=False)["unidades"].sum().sort_values("fecha_mes"))

    if plot:
        plt.figure()
        plt.plot(nuevo_df["fecha_mes"], nuevo_df["unidades"], marker="o")
        plt.title(f"Evolución mensual – {codigo_producto}")
        plt.xlabel("Mes")
        plt.ylabel("Unidades")
        plt.tight_layout()
        plt.show()

    return nuevo_df

#TEST:
# pedidos, clientes, incidencia = cargar_datos("pedidos-2.csv","clientes.csv","incidencia.csv")
# # print(evolucion_producto(pedidos, "F001"))
# print(evolucion_producto(pedidos, "F003", plot=True))

def comparar_productos(df_pedidos, codigos_productos, plot = False):

    #Verificamos si solo se admite una lista.

    if not isinstance(codigos_productos, list):
        #Aviso por si a alguien se le ocurre meter algo que no sea una lista en la función. No devuelve nada y salta el error
        print("El input codigos_productos debe ser una lista, la función COMPARAR PRODUCTOS se detiene")
        return None
    df = df_pedidos.copy()

    # Filtrar solo los productos seleccionados
    df = df[df["producto_id"].isin(codigos_productos)]

    # Agrupar por producto y mes el promedio de unidades
    tabla = (df.groupby(["producto_id", "mes"], as_index=False)["unidades"].mean().rename(columns={"unidades": "unidades_promedio"}))
    diccionario_de_meses = {1: "Ene", 2: "Feb", 3: "Mar", 4: "Abr",5: "May", 6: "Jun", 7: "Jul", 8: "Ago",9: "Sep", 10: "Oct", 11: "Nov", 12: "Dic"}
    print (tabla)
    #.map busca el valor equivalente de cada número en el diccionario y lo reemplaza
    #Entonces creamos una columna que se llame mes_nombre, la cual asigne como valores
    #los que haya en el diccionario_de_meses, cuando las claves coincidan con las de la columna mes, ya que cada mes es un numero en esa columna.
    tabla["mes_nombre"] = tabla["mes"].map(diccionario_de_meses)

    # Renombrar a unidades_promedio
    tabla = tabla.rename(columns={"unidades": "unidades_promedio"})
    print(tabla)
    if plot:
        plt.figure()
        plt.plot(tabla["mes"], tabla["unidades_promedio"], marker="o")
        plt.xticks(range(1, 13), [pd.Timestamp(2000, m, 1).strftime("%b") for m in range(1, 13)])
        plt.title(f"Estacionalidad – {codigos_productos}")
        plt.xlabel("Mes")
        plt.ylabel("Unidades promedio")
        plt.tight_layout()
        plt.show()

    return tabla[["mes", "mes_nombre", "unidades_promedio"]]

#TEST
# df = pd.read_csv("pedidos-2.csv")
# df = convertir_fecha(df)
# tabla_resultado = comparar_productos(df,  ["F002", "F008", "F012"], plot=True)
# # tabla_resultado = comparar_productos(df, 5, plot=True)

def estacionalidad_productos(df_pedidos, codigo_producto, plot=False):
    
    tabla_de_codigos = df_pedidos['producto_id'].unique()
    #Si se pone como input un  codigo del producto que no esté en la lista, entonces salta error
    if codigo_producto not in tabla_de_codigos:
        print("Ese código de producto no existe, la funcion ESTACIONALIDAAD_PRODUCTOS se detiene")
        return None
    #Filtramos el producto
    df = df_pedidos[df_pedidos["producto_id"] == codigo_producto].copy()

    # Promedio por mes (ignorando años)
    tabla = df.groupby("mes", as_index=False)["unidades"].mean()
    # print (tabla)
    # Asegurar que salgan todos los meses del 1 al 12
    todos_los_meses = pd.DataFrame({"mes": list(range(1, 13))})
    #Cogemos el dataframe ded todos_los_meses lo metemos en la tabla en la columna mes, (on = mes es la clave que se usa para el merge) .
    tabla = todos_los_meses.merge(tabla, on="mes")
    tabla["unidades"] = tabla["unidades"].fillna(0)

    # Volvemos a mapear en la nueva columna mes_hombre los datos del diccionario_de_meses cuyas claves coincidan con los  datos de la columna mes
    diccionario_de_meses = {1: "Ene", 2: "Feb", 3: "Mar", 4: "Abr",5: "May", 6: "Jun", 7: "Jul", 8: "Ago",9: "Sep", 10: "Oct", 11: "Nov", 12: "Dic"}
    tabla["mes_nombre"] = tabla["mes"].map(diccionario_de_meses)

    # Renombrar a unidades_promedio para que quede claro que es un promedio
    tabla = tabla.rename(columns={"unidades": "unidades_promedio"})

    # Gráfico opcional
    if plot:
        plt.figure()
        plt.plot(tabla["mes"], tabla["unidades_promedio"], marker="o")
        plt.xticks(range(1, 13), [diccionario_de_meses[i] for i in range(1, 13)])
        plt.title(f"Estacionalidad del producto {codigo_producto}")
        plt.xlabel("Mes")
        plt.ylabel("Unidades (promedio)")
        plt.tight_layout()
        plt.show()

    return tabla[["mes", "mes_nombre", "unidades_promedio"]]

df = pd.read_csv("pedidos-2.csv")
df = convertir_fecha(df)
#tabla_resultado = estacionalidad_productos(df,  53, plot=True)
# tabla_resultado = estacionalidad_productos(df,  "F003", plot=True)

def pedidos_por_zona(df_pedidos, df_clientes):
   
    # Nos quedamos solo con lo necesario para el cruce
    
    clientes_min = df_clientes[["cliente_id", "zona"]].copy()

    # Unimos zona a cada línea de pedido
    df = df_pedidos.merge(clientes_min, on="cliente_id")


    #Agregamos la columna pedido_id y le aplicamos la funcion nunique, y luego la columnaa unidades y le aplicamos la suma.
    #Luego agrupamos eso por zonas
    tabla = (df.groupby("zona", as_index=False).agg(pedidos_totales=("pedido_id", "nunique"),unidades_totales=("unidades", "sum")))
   
    return tabla

# TEST:
# clientes = pd.read_csv("clientes.csv")
# pedidos = pd.read_csv("pedidos-2.csv")
# tabla = pedidos_por_zona(pedidos, clientes)
# print(tabla)

def demanda_vs_poblacion(df_pedidos, df_clientes, listado_productos = None):
    
    # Cruce básico con zona y población
    base_clientes = df_clientes[["cliente_id", "zona", "poblacion_objetivo"]]
    df = df_pedidos.merge(base_clientes, on="cliente_id", how="left")

    # Filtrar por productos si se se pasa como input un listado de productos. Si es así, se añade esa columna, sino no.
    if listado_productos is None:
        tabla = df.groupby(["zona", "poblacion_objetivo"], as_index=False)["unidades"].sum()
        
    else:
        df = df[df["producto_id"].isin(listado_productos)]
        tabla = df.groupby(["zona", "producto_id", "poblacion_objetivo"], as_index=False)["unidades"].sum()

    # Calcular ratio por 1000 habitantes y evitamos el caso en el que se divida entre 0
    tabla["unidades_por_1000"] = 0.0
    #Fijamos la variable mayor_que_0 con un TRUE
    mayor_que_0 = (tabla["poblacion_objetivo"] > 0)
    #Aplicamos la operacion solo a las filas en las que mayor_que_0 sea TRUE
    tabla.loc[mayor_que_0, "unidades_por_1000"] = (tabla.loc[mayor_que_0, "unidades"] / tabla.loc[mayor_que_0, "poblacion_objetivo"]) *1000

    # Ordenamos los valores, comprobando si nos han pasado algo de input en lista de productos
    if listado_productos is None:
        tabla = tabla.sort_values("unidades_por_1000")
    else:
        tabla = tabla.sort_values(["producto_id", "unidades_por_1000"])

    #Devuelve la tabla y resetea el índice y lo dropea
    return tabla.reset_index(drop=True)

# TEST:
# clientes = pd.read_csv("clientes.csv")
# pedidos = pd.read_csv("pedidos-2.csv")
# incidencia = pd.read_csv("incidencia.csv")
# demanda_y_poblacion_tabla = demanda_vs_poblacion(pedidos, clientes)
# demanda_y_poblacion_tabla = demanda_vs_poblacion(pedidos, clientes, ["F001","F002"])
# print(demanda_y_poblacion_tabla.head(10))

def estacionalidad_enfermedad(df_marcadores, plot = False):

    df = df_marcadores.copy()

    #Hacemos una lista con las columnas_de_tasa.  En ella recorremos con un bucle las columnas del df, 
    # y añadiremos a la lista las que empiecen con tasa_
    #En el data frame de incidencia.csv
    columnas_de_tasa = []
    for i in df.columns:
        if str(i).startswith("tasa_"):
            columnas_de_tasa.append(i)

    if "mes" not in df.columns:
        if "fecha" not in df.columns:
            print("Falta la columna 'mes' y tampoco existe la columna 'fecha'")
            return None 
        df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
        df["mes"] = df["fecha"].dt.month
    # if len(columnas_de_tasa) == 0:
    #     print("No hay columnas que empiecen por 'tasa_' en el DataFrame, la funcion ESTACIONALIDAD_ENFERMEDAD se detiene")
    #     return None

    #Promedio por mes 
    tabla = df.groupby("mes", as_index=False)[columnas_de_tasa].mean()

    #Aseguramos que aparecen todos los meses del 1 al 12
    meses = pd.DataFrame({"mes": list(range(1, 13))})
    tabla = meses.merge(tabla, on="mes")
    for i in columnas_de_tasa:
        tabla[i] = tabla[i].fillna(0)

    #Si plot = TRUE, entonces se muestra el gráfico
    if plot == True:
        plt.figure()
        for i in columnas_de_tasa:
            plt.plot(tabla["mes"], tabla[i], marker="o", label=i)
        plt.xticks(range(1, 13))
        plt.title("Estacionalidad de enfermedades (promedio mensual)")
        plt.xlabel("Mes")
        plt.ylabel("Tasa promedio")
        plt.legend()
        plt.tight_layout()
        plt.show()

    return tabla

# TEST:
# incidencia = pd.read_csv("incidencia.csv")
# # matriz_consumo  = estacionalidad_enfermedad(incidencia, plot = False)
# # print(matriz_consumo)
# matriz_consumo  = estacionalidad_enfermedad(incidencia, plot = True)
# print(matriz_consumo)

def pedidos_vs_incidencia(df_pedidos, df_marcadores, farmaco_id,  enfermedad, plot=False):

    pedidos = df_pedidos.copy()
    marcadores = df_marcadores.copy()

    # Asegurar que esté fecha_mes en ambos dataframes

    if "fecha_mes" not in pedidos.columns:

        #Errors coerce se  usa para convertir los objetos que no se pueden convertir en fecha  y hora a NaT
        pedidos["fecha"] = pd.to_datetime(pedidos["fecha"], errors="coerce")

        #Convertimos a mes y al inicio dedl periodo (timestamp)
        pedidos["fecha_mes"] = pedidos["fecha"].dt.to_period("M").dt.to_timestamp()
    if "fecha_mes" not in marcadores.columns:

        marcadores["fecha"] = pd.to_datetime(marcadores["fecha"], errors="coerce")

        marcadores["fecha_mes"] = marcadores["fecha"].dt.to_period("M").dt.to_timestamp()

    # Aseguramos que la columna de enfermedad exista 
    if enfermedad not in marcadores.columns:
        print("La columna introducida en la función de 'enfermedad' no existe en  el dataframe")
        return None
    
    # Serie mensual del fármaco
    serie_f = (pedidos[pedidos["producto_id"] == farmaco_id].groupby("fecha_mes", as_index=False)["unidades"].sum().rename(columns={"unidades": "unidades_farmaco"}))

    # Serie mensual de la enfermedad con promedio por zonas
    serie_e = (marcadores.groupby("fecha_mes", as_index=False)[enfermedad].mean().rename(columns={enfermedad: "incidencia"}))

    # Se une por mes con clave 'fecha_mes'
    tabla = serie_f.merge(serie_e, on="fecha_mes").sort_values("fecha_mes")

    # Gráfico opcional (puntos + recta sencilla)
    if plot == True:
        plt.scatter(tabla["incidencia"], tabla["unidades_farmaco"])

        #Quitamos las filas donde falte uncidencia o unidades_farmaco
        datos = tabla.dropna(subset=["incidencia", "unidades_farmaco"])
        #Necesitamos 2 puntos válidos para ajustar la recta de regresión. 
        # m es la pendiente, b es la ordenada en el origen. con forma y = mx + b
        if len(datos) >= 2:

            #La funcion polyfit calcula la mejorr recta que se ajusta a esos dos puntos.
            #Además incidamos  1 como input a polyfit porque el polinomio de la recta es de  grado 1 (y = mx + b)
            m, b = np.polyfit(datos["incidencia"], datos["unidades_farmaco"], 1)

            #Crea 100 valores de x con espacios iguales entre el minimo y el máximo de incidencias
            x = np.linspace(datos["incidencia"].min(), datos["incidencia"].max(), 100)

            #Definimos la recta
            y = m * x + b

        plt.plot(x, y)
        plt.title(f"{farmaco_id}: Unidades vs {enfermedad}")
        plt.xlabel(enfermedad)
        plt.ylabel("Unidades del fármaco")
        plt.tight_layout()
        plt.show()

    return tabla.reset_index(drop=True)

# # TEST: 
# incidencia = pd.read_csv("incidencia.csv")
# pedidos = pd.read_csv("pedidos-2.csv")

# #correlacion_incidentes = pedidos_vs_incidencia(pedidos, incidencia, 'F001', 'gripe')

# #correlacion_incidentes = pedidos_vs_incidencia(pedidos, incidencia, "F002", "tasa_gripe")

# correlacion_incidentes = pedidos_vs_incidencia(pedidos, incidencia, "F001", "tasa_gripe", plot=True)

# print(correlacion_incidentes)