'''
   empresa:
      Administra los datos de las empresas clientes de Venaycia.com 

   copyright 2021 - Vitt Inversiones SAS - vitt.co:
      licensed to Velasquez Naranjo y Cia SAS - Venaycia.com
   author: Wiliam Arévalo Camacho
'''
from src import app
from src.utility import validator
from src.model import empresa
from flask import jsonify, request

@app.route('/company', methods = ['POST'])
def createCompany():
   '''
       createCompany: Recibe los datos de una empresa cliente para guardarlos en la DB \n
   '''
   ## Validad que se enviarion todos los campos
   if not 'nit' in request.json:
      return {'response':'ERROR', 'message': 'NIT es obligatorio, por favor verifíque'}
   if not 'nombre' in request.json:
      return {'response':'ERROR', 'message': 'Nombre de la empresa es obligatorio, por favor verifíque'}
   dato = request.json
   print("In createCompany:", dato['nit'])
   if not dato['nit']:
      return {'response':'ERROR', 'message': 'NIT es obligatorio, por favor verifíque'}
   if not dato['nombre']:
      return {'response':'ERROR', 'message': 'Nombre de la empresa es obligatorio, por favor verifíque'}
   
   ## Guarda una nueva empresa en la DB
   resp = empresa.addCompany(dato)
   return jsonify(resp)

@app.route('/files/<company>', methods = ['POST'])
def manageFiles(company):
   '''
       createUsers: Recibe los archivo de los empleador de una empresa para guardarlos en la DB \n
       @params: 
         company: Contiene el identificador de la empresa
   '''
   print("In manageFiles:", company)
   ## Valida que se enviarion todos los campos
   if not 'usuarios' in request.files:
      return {'response':'ERROR', 'message': 'No se recibió el archivo de usuarios, por favor verifíque'}
   if not 'frecuencias' in request.files:
      return {'response':'ERROR', 'message': 'No se recibió el archivo de frecuencias, por favor verifíque'}
   if not 'diccionario' in request.files:
      return {'response':'ERROR', 'message': 'No se recibió el archivo de diccionario, por favor verifíque'}
   ## Obtiene los archivos del request
   usuarios    = request.files['usuarios']
   diccionario = request.files['diccionario']
   frecuencias = request.files['frecuencias']
   ## Valida que se agregaron todos los archivos
   if usuarios.filename == '':
      return {'response':'ERROR', 'message': 'No se seleccionó el archivo de usuarios, por favor verifíque'}
   if diccionario.filename == '':
      return {'response':'ERROR', 'message': 'No se seleccionó el archivo de diccionario, por favor verifíque'}
   if frecuencias.filename == '':
      return {'response':'ERROR', 'message': 'No se seleccionó el archivo de frecuencias, por favor verifíque'}
   ## Valida que todos los archivos son de tipo excel
   if not validator.validateExcel(usuarios.filename):
      return jsonify({'response': 'ERROR', 'message': 'El archivo usuarios no es de tipo Excel'})
   if not validator.validateExcel(diccionario.filename):
      return jsonify({'response': 'ERROR', 'message': 'El archivo diccionario no es de tipo Excel'})
   if not validator.validateExcel(frecuencias.filename):
      return jsonify({'response': 'ERROR', 'message': 'El archivo frecuencias no es de tipo Excel'})
   
   dic = empresa.addDiccionario(diccionario, company, 4)
   return dic