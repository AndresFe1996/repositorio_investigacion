# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 19:10:44 2023

@author: Home
"""

import pandas as pd

"""PRESENTACION:
se descarga los datos de datos.gov sobre las tasas de intereses de diferentes establecimientos
en coloombi desde el 2021 hasta principios del 2023, se cuenta con 19 columnas
las cuales detallan, tipo de entidad, nombre de entidad, fecha de corte etc

se desea establecer para las fechas de diciembre del 2022 hasta marzo del 2023 lo siguiente:
    
1. que tipo de entidades son las que mas prestan en colombia?
2. que entidades son las que mas prestan en colombia
3. cuales son los plazos con mayores prestamos establecidos
4. que sexos son los que mas piden prestado en colombia
5. que tipos de personas tienen mayor participacion en este periodo
6. que productos son los mas notables
"""

## Limpieza de datos ##

#importar la base de datos a estudiar
tasas=pd.read_csv("D:/DOCUMENTOS/cosas hechas por mi/python/proyectos pyhton/Bases_de_datos_practicas/Tasas_de_inter_s_activas_por_tipo_de_cr_dito.csv",parse_dates=(["Fecha_Corte"]))

# revision preliminar de la informacion
print("dimensiones del DF",tasas.shape)
tasas.head()

# revision del tipo de datos del DF
tasas.info()

"""se evidencia algunos datos faltantes en el set de datos se va a proceder con la limpieza"""

"""# La limpieza de datos se puede dar por:
    
   1. datos faltantes en celdas
   2. columnas irrelevantes para el estudio
   3. registros repetidos
   4. valores extremos o outliers (aunque se debe revisar bien la definicion y
                                   el set)
   5.errores tipograficos en las variables categorias 
   
tambien debemos agregar los errores par alos tipos int y float ya que dependiento de que
estamos estudiando, los valores con su naturaleza +/- podriar ser tambien errores
    
    """
## seleccionamos las columnas relevantes para el estuido
    
tasas_relevante=tasas[["Nombre_Tipo_Entidad","Nombre_Entidad","Fecha_Corte",
                       "Unicap","Descrip_Unicap","(1)Tipo_de_persona","(2)Sexo",
                       "(3)Tamaño_de_empresa","(4)Tipo_de_crédito","(6) Producto de crédito",
                       "(7) Plazo de crédito","(10)Montos_desembolsados","(11)Número_de_créditos_desembolsados"
                       ]]    

tasas_relevante.info()
# quitar datos faltantes
tasas_relevante.dropna(inplace=True) # quitar datos faltantes
tasas_relevante.info()

"""de 179306 renglones iniciales se registran ahora 176666 que cumplen con completitud"""

# verifiquemos que las columnas categorias tengan varios subniveles o por lo menos
# cumplen con la idea de categoria

cols_cat=["Nombre_Tipo_Entidad","Nombre_Entidad","Descrip_Unicap",
          "(1)Tipo_de_persona","(2)Sexo","(3)Tamaño_de_empresa","(4)Tipo_de_crédito",
          "(6) Producto de crédito","(7) Plazo de crédito"]

for col in cols_cat:
    print(f'columna {col}:{tasas_relevante[col].nunique()} subniveles')


"""detectamos que la columna descrip_unicap es menor o igual a 1 por tanto es una
columna que no es necesario, no la vamos a retirar pero en teoria es una colummna irrelevante"""


# revisemos los datos numericos

tasas_relevante.describe()

"""observamos que la desviacion estandar std son diversos excepto para unicap, porque es una columna
que tiene solo valores 1"""

# filas repetidas

print(f'set de datos con: {tasas_relevante.shape}')
tasas_relevante.drop_duplicates(inplace=True) #eliminamos las filas repetidas
print(f'set de datos con: {tasas_relevante.shape}')

"""se eliminan 245 filas repetidas"""

# outliers en valores numericos
# importamos las librerias matplotlib y seaborn
import matplotlib.pyplot as plt
import seaborn as sns

# traemos las columnas numericas que vamos a analizar
cols_num=["Unicap","(10)Montos_desembolsados","(11)Número_de_créditos_desembolsados"]

# creamos un grafico vacio, con 3 filas en una sola columna
fig, ax=plt.subplots(nrows=3, ncols=1,figsize=(8,30)) # nrows son el numero de variables
# a tener en cuenta
fig.subplots_adjust(hspace=0.5)

# con un bucle incertamos en los graficos vacios los datos a mostrar
for i,col in enumerate(cols_num):
    sns.boxplot(x=col,data=tasas_relevante,ax=ax[i])
    ax[i].set_title(col)
    
"""unicap presenta un comportamiento de linea horizontal, esto es producto a que la variable
no tiene valores que cambien,  montos desembolsados presenta un problema de formato ya
que aparecen con float pero son numeros tan grandes que salen en notacion cientifica"""
        
    
## QUITAR ERRORES EN VARIBALES TIPOGRAFICAS

"""cols_cat=["Nombre_Tipo_Entidad","Nombre_Entidad",
          "(1)Tipo_de_persona","(2)Sexo","(3)Tamaño_de_empresa","(4)Tipo_de_crédito",
          "(6) Producto de crédito","(7) Plazo de crédito"]

fig, ax =plt.subplots(nrows=8,ncols=1, figsize=(10,30))
fig.subplots_adjust(hspace=1)

for i,col in enumerate(cols_cat):
    sns.countplot(x=col, data=tasas_relevante, ax=ax[i])
    ax[i].set_title(col)
    ax[i].set_xticklabels(ax[i].get_xticklabels(),rotation=0)"""

"""debido a la presencia enorme de variables categoricas este tipo de graficos no es posible
graficarlos de manera normal por tanto vamos a proceder a graficarlos de manera 
individual e ir al detalle uno a uno."""
## revision nombre_tipo_entidad
fig, ax=plt.subplots(nrows=1,ncols=1,figsize=(15,20))
sns.countplot(x="Nombre_Tipo_Entidad",data=tasas_relevante,ax=ax)
"""se observa que no existe variabilidad o posibles variables categoricas mal codificadas
asi mismo, el conteo refleja una mayor y casi superior participacion de entidades del
tipo bancario, esto se confirmara en la fase de EDA"""

## revision nombre_entidad
# aqui debemos usar barplot ya que countplot no es invertible y por tanto
# tendremos un serio problema en la visualizacion de las entidades
conteo_nombre_entidades=tasas_relevante["Nombre_Entidad"].value_counts().reset_index()
conteo_nombre_entidades.columns=["Entidad","Conteo"]
plt.figure(figsize=(8,6))
sns.barplot(x="Conteo",y="Entidad", data=conteo_nombre_entidades)
# editar el grafico
plt.title("conteo nombre entidades")
plt.xlabel("conteos")
plt.ylabel("entidades")
# mostrar el grafico
plt.show()
"""no se evidencia error en nombres de entidades, asi mismo se evidencia que bancolombia
es la entidad con mas conteos en el data set, se vera mas a fondo en el EDA"""

# revision tipo de persona
fig, ax=plt.subplots(nrows=1,ncols=1,figsize=(15,20))
sns.countplot(x="(1)Tipo_de_persona",data=tasas_relevante,ax=ax)

"""no se evidencia error en la variable de tipo de persona"""

# revision sexo
fig, ax=plt.subplots(nrows=1,ncols=1,figsize=(15,20))
sns.countplot(x="(2)Sexo",data=tasas_relevante,ax=ax)
"""se evidencia 4 categorias pero estan de acuerdo para su uso pues no suponen erores
de tipo escritura"""

# revision tamaño de la empresa
fig, ax=plt.subplots(nrows=1,ncols=1,figsize=(15,20))
sns.countplot(x="(3)Tamaño_de_empresa",data=tasas_relevante,ax=ax)
"no se evidencia errores en la variable"

# revision tipo de credito
fig, ax=plt.subplots(nrows=1,ncols=1,figsize=(15,20))
sns.countplot(x="(4)Tipo_de_crédito",data=tasas_relevante,ax=ax)
"no se evidencia errores en esta variable"

# revision producto de credito
# esta variable tambien tenemos problemas por la cantidad, procedemos a hacer un 
# arreglo similar al ue hicimos en entidades

conteo_tipo_producto=tasas_relevante["(6) Producto de crédito"].value_counts().reset_index()
conteo_tipo_producto.columns=["Tipo producto credito","Conteo"]
plt.figure(figsize=(20,40))
sns.barplot(x="Conteo",y="Tipo producto credito", data=conteo_tipo_producto)
# editar el grafico
plt.title("conteo tipo productos")
plt.xlabel("conteos")
plt.ylabel("productos")
# mostrar el grafico
plt.show()

"""no se detecta errores tipograficos"""

# (7) Plazo de crédito
# misma situacion por la cantidad de conteos, se realiza arreglo

conteo_tipo_producto=tasas_relevante["(7) Plazo de crédito"].value_counts().reset_index()
conteo_tipo_producto.columns=["plazo credito","Conteo"]
plt.figure(figsize=(20,40))
sns.barplot(x="Conteo",y="plazo credito", data=conteo_tipo_producto)
# editar el grafico
plt.title("conteo plazos creditos")
plt.xlabel("conteos")
plt.ylabel("plazo credito")
# mostrar el grafico
plt.show()

"""no tenemos errores"""

"""finalizamos la limpieza pues no se detectaron mas errorres, vamos a guardar el dataset
limpio para su manipulacion en el proximo paso del proyecto que sera el EDA
o analisis exploratorio de los datos"""

"""
IDEAS A TENER CLARO CON EL EDA

Tener clara la pregunta que queremos responder;
Tener una idea general de nuestro dataset;
Definir los tipos de datos que tenemos;
Elegir el tipo de estadística descriptiva
Visualizar los datos;
Analizar las posibles interacciones entre las variables del dataset; y finalmente
Extraer algunas conclusiones de todo este análisis."""

"""realizada la parte de limpieza de datos procedemos a responder las preguntas:
    1. que tipo de entidades son las que mas prestan en colombia en montos y que entidades
    prestan mas en cantidad de creditos?
    2. cuales son los plazos con mayores prestamos establecidos en montos y cantidades
    3. que sexos son los que mas piden prestado en colombia en monto y cantidades
    4. que tipos de personas tienen mayor participacion en este periodo
    5. que productos son los mas notables
    6. Existe alguna epoca del año donde los montos crezcan mas?
 """


"""1. que tipo de entidades son las que mas prestan en colombia en montos y que entidades
    prestan mas en cantidad de creditos?
    """
# procedemos a cambiar el formato de la columna monto pues como vimos antes
# esta columna esta un poco mal vista por la notacion cientifica asi que vamos 
# a colocar una nuenva columna que nos permita tomar monto y verla en una vista de 
# de miles de millones
tasas_relevante.info()
miles_de_millones=1_000_000_000
tasas_relevante["monto-miles_de_millones"]=tasas_relevante["(10)Montos_desembolsados"]/miles_de_millones

# tambien vamos a cambiar el la columna # numero de creditos ya que las cifras
# al sumarse nos daran una pesima presentacion por la notacion cientifica, vamos
# a proceder a dejar los prestamos en terminos de 5.000 es decir
# cada entidad va prestar el valor sobre 5.000 unidades

diez_mil=5_000
tasas_relevante["cantidades-5000_unidades"]=tasas_relevante["(11)Número_de_créditos_desembolsados"]/diez_mil


data=tasas_relevante[["Nombre_Tipo_Entidad","monto-miles_de_millones","cantidades-5000_unidades"]]

agregados=data.groupby("Nombre_Tipo_Entidad").sum()

# Crear figura y ejes y configuracion del tamaño
fig, ax1 = plt.subplots(figsize=(20,10))

# Graficar los montos como barras en el eje primario
ax1.bar(agregados.index, agregados['monto-miles_de_millones'], color='blue')
ax1.set_xlabel('Tipo Entidad')
ax1.set_ylabel('Monto en miles de millones', color='blue')
ax1.tick_params('y', colors='blue')

# Crear un segundo eje para el número de préstamos
ax2 = ax1.twinx()
ax2.plot(agregados.index, agregados['cantidades-5000_unidades'], color='red', marker='o')
ax2.set_ylabel('Número de Préstamos en 5000 unidades', color='red')
ax2.tick_params('y', colors='red')

# Establecer título
plt.title('Montos y Número de Préstamos por tipo de Entidad')
# Mostrar el gráfico
plt.show()

# ahora que entidades son los que mas prestan en colombia?
tasas_relevante.info()
data_entidad=tasas_relevante[["Nombre_Entidad","cantidades-5000_unidades","monto-miles_de_millones"]]

# crear el df de los datos a utilizar
agregados_entidad=data_entidad.groupby("Nombre_Entidad").sum()
agregados_entidad_2=agregados_entidad.reset_index()

# crear la grafica - de barras horizontal debido a la cantidad de variables
# categoricas

plt.barh(agregados_entidad_2["Nombre_Entidad"],agregados_entidad_2["monto-miles_de_millones"],label='Montos prestados en miles de millores')
plt.barh(agregados_entidad_2["Nombre_Entidad"],agregados_entidad_2["cantidades-5000_unidades"],label='Montos por cada 5000 unidades')

# agregar etiquetas de datos a cada barra
"""
for i, v in enumerate(agregados_entidad_2['monto-miles_de_millones']):
    plt.text(v + 10, i, str(v), color='black')
for i, v in enumerate(agregados_entidad_2['cantidades-5000_unidades']):
    plt.text(v + 0.1, i, str(v), color='black')
"""
# Establecer título y leyendas
plt.title('Montos en miles de millores y Número de Créditos Prestados por Entidad en 5000 unidades')
plt.xlabel('Valor')
plt.ylabel('Entidad')
plt.legend()
plt.show()

# para presentacion se deja una tabla con la lista de entidades

tabla_1=agregados_entidad_2.sort_values(['monto-miles_de_millones',"cantidades-5000_unidades"], ascending=False)
print(tabla_1)

"""las entidades que mas venden en colombia es sin duda las establecimientos bancarios
llegando a casi $484.007 miles de millones en montos desembolsados, tambien figuran
como los tipos con mas numero de desembolsos realizados pues estan sobre las 77.242.8 unidades por 5000 unidades
lo que sin duda los convierte en el sector financiero como las entidades que mas dinero mueven

por otro lado, bancolombia es la entidad con mas montos y numero de desembolsos realizados, le siguen banco davivienda,
scotiabank y banco falabella


"""

"""2. cuales son los plazos con mayores prestamos establecidos en montos y cantidades?"""
data_plazos=tasas_relevante[["(7) Plazo de crédito","monto-miles_de_millones","cantidades-5000_unidades"]]

agregados_plazos=data_plazos.groupby("(7) Plazo de crédito").sum()
agregados_plazos_2=agregados_plazos.reset_index()

plt.figure(figsize=(20,20))

plt.barh(agregados_plazos_2["(7) Plazo de crédito"],agregados_plazos_2["monto-miles_de_millones"],label='Montos prestados en miles de millores')
plt.barh(agregados_plazos_2["(7) Plazo de crédito"],agregados_plazos_2["cantidades-5000_unidades"],label='Montos por cada 5000 unidades')

# Establecer título y leyendas
plt.title('Montos en miles de millores y Número de Créditos Prestados por plazos en 5000 unidades')
plt.xlabel('Valor')
plt.ylabel('plazo del credito')
plt.legend()
plt.show()


"""se observa que para los plazos, el de consumo de 1 mes representa el mas curioso
pues su cantidad de prestamosx5000 unidades y los montos se sobreponen, lo que significa
que las cantidades son mucho mayores a los montos prestamose n miles de millones

le siguen los avances en efectivo donde los montos son mas grandes que las cantidades y
consumos entre 2 y 6 meses le siguen

consideraciones importantes: el consumo es lo que mas se mueve entre todos los distintos
plazos
"""

""" 3. que sexos son los que mas piden prestado en colombia en monto y cantidades"""
data_sexo_rel=tasas_relevante[["(2)Sexo","monto-miles_de_millones","cantidades-5000_unidades"]]

# filtrar la columna sexo para que no salgan NO aplica
tipos_deseados=["Masculino","Femenino","No binario"]
data_sexo_fil=data_sexo_rel[data_sexo_rel["(2)Sexo"].isin(tipos_deseados)]# aqui filtramos la informacion que queremos usando isin

agregados_sexo=data_sexo_fil.groupby("(2)Sexo").sum()
data_sexo_rel_2=data_sexo_fil.reset_index()

data_sexo_rel_2.drop("index",axis=1 , inplace=True)
data_sexo_rel_2.head()

# vamos a agrupar la informacion del df filtrado
grupo_genero=data_sexo_rel_2.groupby("(2)Sexo").agg({"monto-miles_de_millones":"sum",
                                                    "(2)Sexo":"count"})

grupo_genero.columns=["Suma de montos en miles de millones","conteo de prestamos en 5000 unidades"]
# creamos el grafico
plt.figure(figsize=(8,6))

# grafico de barras para la suma de los montos
plt.subplot(2,1,1) # dos filas, una columna, grafico 1
plt.bar(grupo_genero.index,grupo_genero["Suma de montos en miles de millones"])
plt.title("Suma de montos por genero en miles de millones")
plt.ylabel("Montos prestamos")

# grafica de barras para el conteo de prestamos

plt.subplot(2, 1, 2)  # Dos filas, una columna, gráfico 2
plt.bar(grupo_genero.index, grupo_genero['conteo de prestamos en 5000 unidades'])
plt.title('conteo de prestamos en 5000 unidades')
plt.ylabel('Conteo')

plt.tight_layout()  # Para evitar superposición de títulos y etiquetas
plt.show()

"""de acuerdo a la grafica podemos evidenciar una tendencia hacia el genero
masculino con mas prestamos solicitados en el sector bancario, sin embargo,es de notar
que las diferencias en las cantidades prestadas son pocas, pues analizando el grafico
de conteo podemos ver que la brecha es menor , aun asi, es claro que el sistema
financiero para este periodo de tiempo tuvo mayor participacion en proyectos del genero
masculino."""



" 4. que sexos son los que mas piden prestado en colombia ? "

print(grupo_genero)
"""
el genero masculino es quien tiene mayor particacion en montos y en numero de prestamos
solicitados en este periodo
"""


"""5. que tipos de personas tienen mayor participacion en este periodo"""
tasas_relevante.info()
data_tipo=tasas_relevante[["(1)Tipo_de_persona","monto-miles_de_millones","cantidades-5000_unidades"]]


grupo_tipo=data_tipo.groupby("(1)Tipo_de_persona").sum()

plt.bar(grupo_tipo.index,grupo_tipo["monto-miles_de_millones"])
plt.bar(grupo_tipo.index,grupo_tipo["cantidades-5000_unidades"])
plt.xlabel("valores")
plt.ylabel("montos")
plt.show()
"""
podemos evidenciar que las personas juridicas(empresas) son las que mas montos pidieorn
prestamos, pero, las cantidades fueron mucho menores que las personas naturales (personas)
aqui la relacion se evidencia como inversa pues los montos fueron menores, pero, la cantidad es mucho mayor

"""

"""6. que productos son los mas notables?"""

tasas_relevante.info()


data_tipo_producto=tasas_relevante[["(6) Producto de crédito","monto-miles_de_millones","cantidades-5000_unidades"]]

grupo_tipo_producto=data_tipo_producto.groupby("(6) Producto de crédito").sum()


plt.barh(grupo_tipo_producto.index,grupo_tipo_producto["monto-miles_de_millones"])
plt.barh(grupo_tipo_producto.index,grupo_tipo_producto["cantidades-5000_unidades"])
plt.show()

"""los productos mas notables son """

print(grupo_tipo_producto)

"""
los Sobregiro en cuenta corriente persona jurídica y las tarjetas de credito para ingresos
superiores a 2 SMMLV suponen los 2 mayores productos financieros en el tiempo evaluado.
las cantidades de prestamos si cambian, pues los sobregiros son muy pocos pero los montos
son muchos mas grandes. mientras que la cantidad de prestamos para tarjetas de credito
es mucho mayor


"""

##ANEXOS movimientos en montos por mes
# usamos resample para agrupar por mes la columna fecha_corte
# es importante que la columna a usar este en el formato datetime
datos_por_mes=tasas_relevante.resample("M",on="Fecha_Corte").sum()

# creamos el grafico de la serie
plt.figure(figsize=(10,10))
plt.plot(datos_por_mes.index,datos_por_mes["(10)Montos_desembolsados"],marker="x")
plt.xlabel=("Mes")
plt.ylabel=("Monto")
plt.title("Serie de tiempo por mes")

## # Rotar etiquetas del eje x para que sean legibles
plt.xticks(rotation=45)

plt.grid(True) # Agregar una cuadrícula al gráfico (opcional)

plt.show()

## BASE DE DATOS USADA
ruta_excel_exportacion='D:/DOCUMENTOS/cosas hechas por mi/python/proyectos pyhton/Bases_de_datos_practicas/Base_tasas_final.xlsx'
tasas_relevante.to_excel(ruta_excel_exportacion,index=False)


