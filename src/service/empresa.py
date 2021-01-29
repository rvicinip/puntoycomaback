'''
   empresa:
      Administra los datos de las empresas clientes de Venaycia.com 

   copyright 2021 - Vitt Inversiones SAS - vitt.co:
      licensed to Velasquez Naranjo y Cia SAS - Venaycia.com
   author: Wiliam Arévalo Camacho
'''
from config import DB, MONGO
import traceback
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
   if not 'niveles' in request.json:
      return {'response':'ERROR', 'message': 'Niveles en el diccionario es obligatorio, por favor verifíque'}
   dato = request.json
   print("In createCompany:", dato['nit'])
   if not dato['nit']:
      return {'response':'ERROR', 'message': 'NIT es obligatorio, por favor verifíque'}
   if not dato['nombre']:
      return {'response':'ERROR', 'message': 'Nombre de la empresa es obligatorio, por favor verifíque'}
   if not dato['niveles']:
      return {'response':'ERROR', 'message': 'Niveles en el diccionario es obligatorio, por favor verifíque'}
   ## Guarda una nueva empresa en la DB
   dato['estado'] = 'A' ## A Identifica que la empresa está activa
   resp = empresa.addCompany(dato)
   return jsonify(resp)

@app.route('/company/<idCompany>', methods = ['GET'])
def getCompany(idCompany):
   '''
       getCompany: Recupera los datos de una empresa en la DB \n
       @params: 
         idCompany: Id mongo de la empresa
   '''
   print("In getCompany:", idCompany)
   resp = empresa.getCompanyById(idCompany)
   return jsonify(resp)

@app.route('/company', methods = ['PUT'])
def updateCompany():
   '''
       updateCompany: Actualiza los datos de una empresa en la DB \n
   '''
   if not 'nombre' in request.json:
      return {'response':'ERROR', 'message': 'Nombre de la empresa es obligatorio, por favor verifíque'}
   if not 'niveles' in request.json:
      return {'response':'ERROR', 'message': 'Niveles en el diccionario es obligatorio, por favor verifíque'}
   dato = request.json
   print("In updateCompany:", dato['nit'])
   if not dato['niveles']:
      return {'response':'ERROR', 'message': 'Niveles en el diccionario es obligatorio, por favor verifíque'}
   if not dato['nombre']:
      return {'response':'ERROR', 'message': 'Nombre de la empresa es obligatorio, por favor verifíque'}
   resp = empresa.updateCompany(dato)
   return jsonify(resp)

@app.route('/company/<idCompany>', methods = ['DELETE'])
def deleteCompany(idCompany):
   '''
       deleteCompany: Actualiza una empresa llevandola a estado 'D' de inactiva o eliminada en la DB \n
       @params: 
         idCompany: Id mongo de la empresa
   '''
   print("In deleteCompany:", idCompany)
   dato = {}
   dato['_id'] = idCompany
   dato['estado'] = 'D' ## D Identifica que la empresa está eliminada o inactiva
   resp = empresa.updateCompany(dato)
   return jsonify(resp)

@app.route('/files/<idCompany>/<niveles>', methods = ['POST'])
def manageFiles(idCompany, niveles):
   '''
       manageFiles: Recibe los archivos de una empresa para procesarlos y guardarlos en la DB \n
       @params: 
         idCompany: Id mongo de la empresa
         niveles: Define la cantidad de nivels que tiene el diccionario
   '''
   print("In manageFiles:", idCompany)
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
   try:
      dicc = empresa.addDiccionario(diccionario, idCompany, niveles)
      frec = empresa.addFrecuacia(frecuencias, idCompany)
      usus = empresa.addEmpleados(usuarios, idCompany)
      return {'response': 'OK', 'diccionario': dicc, 'frecuencias': frec, 'empleados': usus}
   except Exception:
      traceback.print_exc()
      return {'response': 'ERROR', 'message': 'Se presentó un error al procesar los archivos'}

@app.route('/files/dictionary/<idCompany>/<niveles>', methods = ['POST'])
def loadDictionary(idCompany, niveles):
   '''
       loadDictionary: Recibe el archivo diccionario de una empresa para guardarlo en la DB \n
       @params: 
         idCompany: Id mongo de la empresa
         niveles: Define la cantidad de nivels que tiene el diccionario
   '''
   print("In loadDictionary:", idCompany)
   ## Valida que se enviarion todos los campos
   if not 'diccionario' in request.files:
      return {'response':'ERROR', 'message': 'No se recibió el archivo de diccionario, por favor verifíque'}
   ## Obtiene los archivos del request
   diccionario = request.files['diccionario']
   ## Valida que se agregaron todos los archivos
   if diccionario.filename == '':
      return {'response':'ERROR', 'message': 'No se seleccionó el archivo de diccionario, por favor verifíque'}
   ## Valida que todos los archivos son de tipo excel
   if not validator.validateExcel(diccionario.filename):
      return jsonify({'response': 'ERROR', 'message': 'El archivo diccionario no es de tipo Excel'})
   try:
      dicc = empresa.addDiccionario(diccionario, idCompany, niveles)
      return {'response': 'OK', 'data': dicc}
   except Exception:
      traceback.print_exc()
      return {'response': 'ERROR', 'message': 'Se presentó un error al procesar el archivo ' + diccionario.filename}

@app.route('/files/employes/<idCompany>', methods = ['POST'])
def loadEmployes(idCompany):
   '''
       loadEmployes: Recibe el archivo empleado de una empresa para procesarlos y guardarlos en la DB \n
       @params: 
         idCompany: Id mongo de la empresa
   '''
   print("In loadEmployes:", idCompany)
   ## Valida que se enviarion todos los campos
   if not 'usuarios' in request.files:
      return {'response':'ERROR', 'message': 'No se recibió el archivo de usuarios, por favor verifíque'}
   ## Obtiene los archivos del request
   usuarios    = request.files['usuarios']
   ## Valida que se agregaron todos los archivos
   if usuarios.filename == '':
      return {'response':'ERROR', 'message': 'No se seleccionó el archivo de usuarios, por favor verifíque'}
   ## Valida que todos los archivos son de tipo excel
   if not validator.validateExcel(usuarios.filename):
      return jsonify({'response': 'ERROR', 'message': 'El archivo usuarios no es de tipo Excel'})
   try:
      usus = empresa.addEmpleados(usuarios, idCompany)
      return {'response': 'OK', 'data': usus}
   except Exception:
      traceback.print_exc()
      return {'response': 'ERROR', 'message': 'Se presentó un error al procesar el archivo ' + usuarios.filename}

@app.route('/files/frecuency/<idCompany>', methods = ['POST'])
def loadFrecuency(idCompany):
   '''
       loadFrecuency: Recibe el archivo frecuencias de una empresa para procesarlo y guardarlo en la DB \n
       @params: 
         idCompany: Id mongo de la empresa
   '''
   print("In loadFrecuency:", idCompany)
   ## Valida que se enviarion todos los campos
   if not 'frecuencias' in request.files:
      return {'response':'ERROR', 'message': 'No se recibió el archivo de frecuencias, por favor verifíque'}
   ## Obtiene los archivos del request
   frecuencias = request.files['frecuencias']
   ## Valida que se agregaron todos los archivos
   if frecuencias.filename == '':
      return {'response':'ERROR', 'message': 'No se seleccionó el archivo de frecuencias, por favor verifíque'}
   ## Valida que todos los archivos son de tipo excel
   if not validator.validateExcel(frecuencias.filename):
      return jsonify({'response': 'ERROR', 'message': 'El archivo frecuencias no es de tipo Excel'})
   try:
      frec = empresa.addFrecuacia(frecuencias, idCompany)
      return {'response': 'OK', 'data': frec}
   except Exception:
      traceback.print_exc()
      return {'response': 'ERROR', 'message': 'Se presentó un error al procesar el archivo ' + frecuencias.filename}

@app.route('/full/company/<idCompany>', methods = ['GET'])
def getCompanyFull(idCompany):
   '''
       getCompanyFull: Recupera todos los datos de una empresa junto con su diccionario, frecuecias y empleados \n
       @params: 
         idCompany: Id mongo de la empresa
   '''
   print("In getCompany:", idCompany)
   resp = empresa.getFullCompanyByNIT(idCompany)
   return jsonify(resp)

@app.route('/full/dictionary/<idCompany>', methods = ['GET'])
def getDictionary(idCompany):
   '''
       getDictionary: Recupera todos los datos de una empresa junto con su diccionario \n
       @params: 
         idCompany: Id mongo de la empresa
   '''
   print("In getDictionary:", idCompany)
   resp = empresa.getDiccionarioByCompany(idCompany)
   return jsonify(resp)

@app.route('/full/frecuency/<idCompany>', methods = ['GET'])
def getFrecuency(idCompany):
   '''
       getFrecuency: Recupera todos los datos de una empresa junto con sus frecuencias \n
       @params: 
         idCompany: Id mongo de la empresa
   '''
   print("In getFrecuency:", idCompany)
   resp = empresa.getFrecuenciasByCompany(idCompany)
   return jsonify(resp)

@app.route('/full/employes/<idCompany>', methods = ['GET'])
def getEmployes(idCompany):
   '''
       getEmployes: Recupera todos los datos de una empresa junto con sus empleados \n
       @params: 
         idCompany: Id mongo de la empresa
   '''
   print("In getDictionary:", idCompany)
   resp = empresa.getEmpleadosByCompany(idCompany)
   return jsonify(resp)
