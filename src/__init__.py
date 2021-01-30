'''
   BPMBackend

   Aplicación para la gestión de la información de BPM que utiliza Venaycia.com en sus líenas de negocio

   :copyright: Vitt Inversiones SAS - vitt.co
   :license: Velasquez Naranjo y Cia SAS - Venaycia.com
   :author: Wiliam Arévalo Camacho

   Made by Vitt in Medelín - Colombia
   The Software use and distribution is under authorization of Venaycia.com
'''
### Se importan los plugins necesarios
from config import SECRET_KEY, MONGO
from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo

### Se instancia la aplicación
app = Flask(__name__)
### Se establece la clave secreta de generación
app.config['secret_key'] = SECRET_KEY
### Configura CORS para acceder al backend
CORS(app)
### Configura los datos de conexión de la DB
app.config['MONGO_URI'] = MONGO
### Inicializa la conexión de la DB
mongo = PyMongo(app)
### Vincular las clases del sistema
from src.service import login, user, empresa
### Versión de la aplicación
__version__ = "1.0.0"