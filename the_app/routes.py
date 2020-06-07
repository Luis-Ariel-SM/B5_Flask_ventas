from the_app import app
from flask import Flask, render_template, request, redirect, url_for
import csv # libreria de Python para trabajar con los ficheros .csv
import sqlite3 # libreria de Python para las base de datos, ver documentacion de python
from the_app.forms import ProductForm

   
@app.route("/") # Decorador en flask para añadir una ruta e inyecta todo el contenido de index en la aplicacion de flask
def index(): # La funcion es standar y forma parte del decorador. Tiene que tener un return

    fVentas = open (app.config['VENTAS'], 'r') # Abriendo fichero csv y guardandolo en la variable fVentas. las rutas relativas a los ficheros
                                        # se dan desde donde se ejecuta la app, no desde donde escriba la ruta. 
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

@app.route ('/paises') # Las app.routes son funciones que se añaden al modulo app pero realmente no es desde aqui que se lanza la aplicacion
def paises():          
  
    region_name = request.values ['region'] # Los request.values son los parametros de GET y POST
    fVentas = open (app.config['VENTAS'],'r')
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

@app.route('/productos')
def productos():
    conn = sqlite3.connect (app.config['BASE_DATOS'])
    cur = conn.cursor()

    query = "SELECT id, tipo_producto, precio_unitario, coste_unitario FROM productos;"
    resultado = cur.execute(query).fetchall()

    conn.close()
    return render_template ('productos.html', productos=resultado)

@app.route('/addproducto', methods=['GET', 'POST'])
def addproduct():
    form = ProductForm(request.form)# inicializando el formulario con request.form para heredar los atributos ya creados en forms.py

    if request.method == 'GET':
        return render_template ('newproduct.html', form=form)
    else:
        if form.validate():#Metodo de validacion propio de flask, para llegar al 'POST' con la informacion dada por el navegador se necesita inicializar el formulario con request.form 
            conn = sqlite3.connect (app.config['BASE_DATOS'])
            cur = conn.cursor()
            query ="INSERT INTO productos (tipo_producto, precio_unitario, coste_unitario) values (?,?,?); "
            datos = (request.values.get ('tipo_producto'), request.values.get ('precio_unitario'), request.values.get ('coste_unitario'))

            cur.execute (query,datos)
        
            conn.commit()
            conn.close()

            return redirect(url_for('productos'))

        else:
            return render_template ('newproduct.html', form=form)
