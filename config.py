import os

### Obtiene la ubicación relativa del directorio de la aplicación
basedir = os.path.abspath(os.path.dirname(__file__))
### Se establece la clave secreta de generación
SECRET_KEY = 'qazokm.369*'
### URL de la conexión de la DB
MONGO = "mongodb+srv://VenaUser:C0l0mbi421@cluster0.0jieb.mongodb.net/BPM?retryWrites=true&w=majority"
### DB Nombre de la DB que utiliza el sistema
DB = 'BPM'
# Lo generado por MongoDB
# client = PyMongo.MongoClient("mongodb+srv://VenaUser:C0l0mbi421@cluster0.0jieb.mongodb.net/BPM?retryWrites=true&w=majority")