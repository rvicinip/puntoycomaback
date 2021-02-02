import os

### Obtiene la ubicación relativa del directorio de la aplicación
basedir = os.path.abspath(os.path.dirname(__file__))
### Se establece la clave secreta de generación
SECRET_KEY = 'F89312C2F1CF2E8428EE4AB3C5968A2B'
### URL de la conexión de la DB
MONGO = "mongodb+srv://VenaUser:C0l0mbi421@cluster0.0jieb.mongodb.net/BPM?retryWrites=true&w=majority"
### DB Nombre de la DB que utiliza el sistema
DB = 'BPM'
### EMAIL_USER Nombre de usuario del correo de donde se envía el mensaje
EMAIL_USER = 'bpmservice.nr@gmail.com'
### EMAIL_KEY Contraseña del correo electrónico
EMAIL_KEY = 'C0l0mbi4#'
# Lo generado por MongoDB
# client = PyMongo.MongoClient("mongodb+srv://VenaUser:C0l0mbi421@cluster0.0jieb.mongodb.net/BPM?retryWrites=true&w=majority")