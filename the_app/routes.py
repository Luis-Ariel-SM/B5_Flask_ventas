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

@app.route('/addproducto', methods=['GET', 'POST']) # Siempre que se haga un alta o modificacion se utilizan los 2 metodos, tienen que ser informados los request.methods
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

@app.route('/modificaproducto',methods=['GET','POST'])
def modifica_producto():
    if request.method == 'GET':
        id = request.values ['id'] # id es el indice 0 en la base de datos, se pedira ese valor

        conn=sqlite3.connect (app.config['BASE_DATOS']) # Estableciendo coneccion con la base de datos
        cur = conn.cursor() # Creando cursor de la coneccion
        query = "SELECT id, tipo_producto, precio_unitario, coste_unitario FROM productos where id = ?;"# Realizando peticion a la base de datos 
        # segun sintaxis de la misma
        cur.execute(query,(id,)) #Si metemos un solo valor dentro de una tupla lo considerara un valor numerico, para se considerado como tupla se le pone la coma detras
        
        fila = cur.fetchone()
        conn.close() 
        if fila: # Si existe la base de datos, me devuelves mi formulario
            form = ProductForm(data={'id': fila[0], 'tipo_producto': fila[1], 'precio_unitario': fila[2], 'coste_unitario': fila[3]}) # Aqui el get viene vacio y hay que crear el formulario e instanciarlo
            form.submit.label.text='Modificar' #Reutilizando el mismo formulario para evitar hacer uno nuevo pero cambiandole a las bravas el label "Aceptar" x "Modificar"
            return render_template('modifica_producto.html', form=form)
        else:# y sino existe me velves a la lista de"productos" tal y como estaba ya que no se pueden hacer cambios.
            return redirect(url_for('productos'))

    else: # Si es POST, lo sera ya que la 2da peticion del formulario es para meter nuevos datos
        form = ProductForm (request.form) # Aqui ya el formulario viene con datos
        if form.validate():
            conn =sqlite3.connect (app.config['BASE_DATOS']) 
            cur = conn.cursor()

            query = 'UPDATE productos SET tipo_producto = ?, precio_unitario = ?, coste_unitario = ? WHERE id = ?;'
            cur.execute(query, (form.tipo_producto.data, form.precio_unitario.data, form.coste_unitario.data, form.id.data))

            conn.commit()
            conn.close()
            return redirect(url_for('productos'))
        else:
            form.submit.label.text='Modificar'
            return render_template('modifica_producto.html', form=form)
            