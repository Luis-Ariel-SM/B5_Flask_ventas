from the_app import app
from flask import Flask, render_template, request, redirect, url_for
import csv # libreria de Python para trabajar con los ficheros .csv
import sqlite3 # libreria de Python para las base de datos, ver documentacion de python
from the_app.forms import ProductForm, ModProductForm

   
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
        return render_template ('newproduct.html', form=form, error_gral = False)
    else:
        if form.validate():#Metodo de validacion propio de flask, para llegar al 'POST' con la informacion dada por el navegador se necesita inicializar el formulario con request.form 
            conn = sqlite3.connect (app.config['BASE_DATOS'])
            cur = conn.cursor()
            query ="INSERT INTO productos (tipo_producto, precio_unitario, coste_unitario) values (?,?,?); "
            datos = (request.values.get ('tipo_producto'), request.values.get ('precio_unitario'), request.values.get ('coste_unitario'))
            try:
                cur.execute (query,datos)        
                conn.commit()
            except Exception as e:
                print ('INSERT - Error en acceso a base de datos: {}'.format(e))
                conn.close()
                return render_template('newproduct.html', form=form, error_gral='Error en acceso a base de datos:{}'.format(e))

            conn.close()
            return redirect(url_for('productos'))

        else:
            return render_template ('newproduct.html', form=form, error_gral = False)

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
            form = ModProductForm(data={'id': fila[0], 'tipo_producto': fila[1], 'precio_unitario': fila[2], 'coste_unitario': fila[3]}) # Aqui el get viene vacio y hay que crear el formulario e instanciarlo
            return render_template ('modifica_producto.html', form=form)
        else:# y sino existe me velves a la lista de"productos" tal y como estaba ya que no se pueden hacer cambios.
            return redirect(url_for('productos'))

    else: # Si es POST, lo sera ya que la 2da peticion del formulario es para meter nuevos datos
        form = ModProductForm (request.form) # Aqui ya el formulario viene con datos
         
        
        if request.form.get('modificar'): # Si la pregunta es 'modificar'...  ('modificar' es un diccionario, por eso se utiliza el .get para ver ese indice)      

            if form.validate(): #...Me lo validas y si va bien me creas query  y tupla_data...
                query = 'UPDATE productos SET tipo_producto = ?, precio_unitario = ?, coste_unitario = ? WHERE id = ?;' # (peticion de 'modificacion' a la base de datos con sintaxis propia de SQlite)
                tupla_data = (form.tipo_producto.data, form.precio_unitario.data, form.coste_unitario.data, form.id.data) # metiendo los datos de estos parametros en una tupla
            else: #...Si no va bien la validacion me devuelves el modifica_producto.html para ver que pasa
                return render_template('modifica_producto.html', form=form)
        else: # Si en vez de 'modificar' la peticion de 'borrar', 
            query = 'DELETE FROM productos WHERE id = ?;'
            tupla_data = (form.id.data,) 

        conn = sqlite3.connect (app.config['BASE_DATOS']) # Abriendo la base de datos
        cur = conn.cursor() # Creando el cursor 

        try: # Si la cosa va bien...
            cur.execute(query, tupla_data) #...executando la modificacion metiendo la lista 'tupla_data' con los nuevos valores modificados
            conn.commit() #...y me la fijas en la base de datos            
        except Exception as e:
            print ('MOD/DEL - Error en acceso a base de datos: {}'.format(e))
        
        conn.close() # vaya la cosa como vaya siempre hay que cerrar la conexion a la base de datos despues de abrirla
        return redirect(url_for('productos'))

            
            