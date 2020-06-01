import csv, sqlite3

filename = "./sales10.csv" # metiendo el fichero en la variable filename 
database = "./data/ventas.db" # metiendo la base de datos en la variable database

conn = sqlite3.connect(database) # conectando la base de datos
cur = conn.cursor() # creando cursor de python que gestiona las bases de datos 

fSales = open (filename, 'r') # abriendo el fichero csv en modo lectura
csvreader = csv.reader(fSales, delimiter=',') # abriendo el reader de python para los csv delimitando con coma los valores del fichero

headerRow = next (csvreader)
print (headerRow)

query = 'INSERT OR IGNORE into productos (tipo_producto, precio_unitario, coste_unitario) values (?,?,?);'
for dataRow in csvreader: 
    tupla_datos = (dataRow[2],float(dataRow[9]),float(dataRow[10]))
    cur.execute(query, tupla_datos)

conn.commit() #Confirmando los cambios en la base de datos, se hace siempre que se modifique la base de datos
conn.close() #Cerrando la coneccion a la base de datos

    
