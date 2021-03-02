'''
   run:
   Arranca la aplicación del servidor 

   :copyright: Vitt Inversiones SAS - vitt.co
   :license: Velasquez Naranjo y Cia SAS - Venaycia.com
   :author: Wiliam Arévalo Camacho
'''
### Se importan los plugins necesarios
from src import app
### arranca  el servidor en el puerto 80
if __name__ == "__main__":
    app.run(debug = True, port = 4000)