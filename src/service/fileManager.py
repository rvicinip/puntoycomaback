'''
   fileManager

   Método generico de acceso a una base de datos en MongoDB definiendo los métodos genrales del CRUD (Create, Read, Update, Delete)

   copyright 2021 - Vitt Inversiones SAS - vitt.co
   licensed by Vitt Inversiones SAS - vitt.co
   author: Wiliam Arévalo Camacho
'''
import pandas as pandas
from src import app

@app.route('/fileManager/usuario', methods = ['POST'])
def createUser(company):
    '''
       :createUser: Crea un usuario de una empresa en la coleeción de usaurio
       :params: company: Contiene el identificador de la empresa
    '''
    print("In createUser:", company)
    dato = request.json
