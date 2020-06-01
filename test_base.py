from flask import Flask
from flask_testing import TestCase
import run

class TestFlaskBase(TestCase): #Clase basica de la cual heredaran nuestros tests
    def create_app(self): #Metodo create_app para iniciar flask
        self.app = run.app #Se guarda la aplicacion en un metodo para luego utilizarla en otros metodos
        return run.app 
        
        
    
    def setUp (self): #Metodo que se lanza antes de los test
        self.client = self.app.test_client() 
        self.client.testing = True

    def tearDown(self):
        pass
