from flask import Flask

app = Flask (__name__, instance_relative_config=True) # Esta es la aplicacion flask, se instancia en la variable app
app.config.from_object('_config') 

from the_app import routes
