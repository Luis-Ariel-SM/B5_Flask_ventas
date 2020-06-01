from flask import Flask, render_template, request
import csv # libreria de Python para trabajar con los ficheros .csv

app = Flask (__name__) # Esta es la aplicacion flask
   
        
@app.route("/") #decorador en flask para añadir una ruta e inyecta todo el contenido de index en la apñicacion de flask
def index(): # La funcion es standar y forma parte del decorador. Tiene que tener un return
    fVentas = open ('./sales10.csv', 'r') # Abriendo fichero csv y guardandolo en la variable fVentas
    csvreader = csv.reader(fVentas, delimiter=',') #procesando el fichero csv guardado en fVentas con la libreria csv de python. La sintaxis es propia de la libreria, ver documentacion.
    registros = []
    d = {} #creando el diccionario
    for linea in csvreader:
        registros.append(linea)
        if linea [0] in d: # Si este valor ya existe en el diccionario
            d[linea[0]]['ingresos'] += float(linea[11]) # Añadele los siguientes valores 
            d[linea[0]]['beneficios'] += float(linea[13])
        else: # y sino
            if linea [0] != 'region':
                d[linea[0]] = {'ingresos': float(linea [11]), 'beneficios': float(linea[13])} # crealos (Es aqui donde se va creando el diccionario y sera el valor de la clave que exista en linea[0])
    
    return render_template ('region.html',ventas=d)

@app.route ('/paises')
def paises():
    region_name = request.values ['region']

    fVentas = open ('./sales10.csv','r')
    cvsreader = csv.reader (fVentas, delimiter =',')
    d = {}
    for linea in cvsreader:
        if linea [0] == region_name:
            if linea [1] in d:
                d[linea[1]]['ingresos'] += float(linea[11])
                d[linea[1]]['beneficios'] += float(linea[13])
            else:
                d[linea[1]] = {'ingresos': float(linea [11]), 'beneficios': float(linea[13])}

    return render_template ('pais.html',ventas_pais=d, region_nm=request.values['region'])
    