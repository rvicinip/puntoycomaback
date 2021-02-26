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
from config import SECRET_KEY, EMAIL_USER, EMAIL_KEY, MYSQL
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

### Se instancia la aplicación
app = Flask(__name__)
### Se establece la clave secreta de generación
app.config['SECRET_KEY'] = SECRET_KEY
### Configura CORS para acceder al backend
CORS(app)
### EMAIL_USER Nombre de usuario del correo de donde se envía el mensaje
app.config['EMAIL_USER'] = EMAIL_USER
### EMAIL_KEY Contraseña del correo electrónico
app.config['EMAIL_KEY'] = EMAIL_KEY
### Configuración de SqlAlchemy para conectarse a la DB de MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = MYSQL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)
### Vincular las clases del sistema
from src.service import login, user, empresa, encuesta
### Versión de la aplicación
__version__ = "1.0.0"