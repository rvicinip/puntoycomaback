'''
   fileManager

   Método generico de acceso a una base de datos en MongoDB definiendo los métodos genrales del CRUD (Create, Read, Update, Delete)

   copyright 2021 - Vitt Inversiones SAS - vitt.co
   licensed by Vitt Inversiones SAS - vitt.co
   author: Wiliam Arévalo Camacho
'''
import pandas as pandas
from src import app
from flask import jsonify, request

@app.route('/fileManager/<company>', methods = ['POST'])
def createUsers(company):
   '''
       createUsers: Recibe un archivo con los usuarios de una empresa para agregarlos a la DB \n
       @params: 
         company: Contiene el identificador de la empresa
   '''
   print("In createUsers:", company)
   archivo = request.files()
   if archivo == None:
      return jsonify({'response': 'ERROR', 'message': 'Los archivos son requeridos para el proceso'})