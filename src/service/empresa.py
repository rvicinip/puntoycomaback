'''
   empresa:
      Administra los datos de las empresas clientes de Venaycia.com 

   copyright 2021 - Vitt Inversiones SAS - vitt.co:
      licensed to Velasquez Naranjo y Cia SAS - Venaycia.com
   author: Wiliam Arévalo Camacho
'''
from flask import jsonify, request
from src import app
from src.model import empresa
from .protector import privated
from src.utility.validator import validateFields, validateFiles
import traceback

@app.route('/company', methods = ['POST'])
@privated
def createCompany(usuario):
   '''
       createCompany: Recibe los datos de una empresa cliente para guardarlos en la DB \n
   '''
   if usuario['perfil'] == 'client':
      return jsonify({'response': 'ERROR', 'message': 'No tiene autorización para realizar esta acción'})
   ## Validad que se enviarion todos los campos
   dato = request.json
   campos = ['nit', 'nombre', 'niveles']
   valida = validateFields(campos, dato)
   if valida['response'] == 'ERROR':
      return jsonify(valida)
   print("In createCompany:", dato['nit'])
   ## Guarda una nueva empresa en la DB
   dato['estado'] = 'A' ## A Identifica que la empresa está activa
   resp = empresa.addCompany(dato)
   return jsonify(resp)

@app.route('/company/<idCompany>', methods = ['GET'])
@privated
def getCompany(usuario, idCompany):
   '''
       getCompany: Recupera los datos de una empresa en la DB \n
       @params: 
         idCompany: Id mongo de la empresa
   '''
   print("In getCompany:", idCompany)
   resp = empresa.getCompanyById(idCompany)
   return jsonify(resp)

@app.route('/company', methods = ['PUT'])
@privated
def updateCompany(usuario):
   '''
       updateCompany: Actualiza los datos de una empresa en la DB \n
   '''
   print("In updateCompany")
   if usuario['perfil'] == 'client':
      return jsonify({'response': 'ERROR', 'message': 'No tiene autorización para realizar esta acción'})
   dato = request.json
   campos = ['_id','nit', 'nombre', 'niveles']
   valida = validateFields(campos, dato)
   if valida['response'] == 'ERROR':
      return jsonify(valida)
   resp = empresa.updateCompany(dato)
   return jsonify(resp)

@app.route('/company/<idCompany>', methods = ['DELETE'])
@privated
def deleteCompany(usuario, idCompany):
   '''
       deleteCompany: Actualiza una empresa llevandola a estado 'D' de inactiva o eliminada en la DB \n
       @params: 
         idCompany: Id mongo de la empresa
   '''
   print("In deleteCompany:", idCompany)
   if usuario['perfil'] == 'client':
      return jsonify({'response': 'ERROR', 'message': 'No tiene autorización para realizar esta acción'})
   dato = {}
   dato['_id'] = idCompany
   dato['estado'] = 'D' ## D Identifica que la empresa está eliminada o inactiva
   resp = empresa.updateCompany(dato)
   return jsonify(resp)

@app.route('/files/<idCompany>/<niveles>', methods = ['POST'])
@privated
def manageFiles(usuario, idCompany, niveles):
   '''
       manageFiles: Recibe los archivos de una empresa para procesarlos y guardarlos en la DB \n
       @params: 
         idCompany: Id mongo de la empresa
         niveles: Define la cantidad de nivels que tiene el diccionario
   '''
   print("In manageFiles:", idCompany)
   if usuario['perfil'] == 'client':
      return jsonify({'response': 'ERROR', 'message': 'No tiene autorización para realizar esta acción'})
   ## Valida que se enviarion todos los campos
   campos = ['usuarios', 'diccionario', 'frecuencias']
   valida = validateFiles(campos, request.files)
   if valida['response'] == 'ERROR':
      return jsonify(valida)
   ## Obtiene los archivos del request y los procesa
   usuarios    = request.files['usuarios']
   diccionario = request.files['diccionario']
   frecuencias = request.files['frecuencias']
   try:
      dicc = empresa.addDiccionario(diccionario, idCompany, niveles)
      if dicc['response'] == 'OK':
         dicc.pop('response')
      frec = empresa.addFrecuacia(frecuencias, idCompany)
      if frec['response'] == 'OK':
         frec.pop('response')
      usus = empresa.addEmpleados(usuarios, idCompany)
      if usus['response'] == 'OK':
         usus.pop('response')
      return jsonify({'diccionario': dicc, 'tiempos': frec, 'usuario': usus})
   except Exception:
      traceback.print_exc()
      return jsonify({'response': 'ERROR', 'message': 'Se presentó un error al procesar los archivos'})

@app.route('/files/dictionary/<idCompany>/<niveles>', methods = ['POST'])
@privated
def loadDictionary(usuario, idCompany, niveles):
   '''
       loadDictionary: Recibe el archivo diccionario de una empresa para guardarlo en la DB \n
       @params: 
         idCompany: Id mongo de la empresa
         niveles: Define la cantidad de nivels que tiene el diccionario
   '''
   print("In loadDictionary:", idCompany)
   if usuario['perfil'] == 'client':
      return jsonify({'response': 'ERROR', 'message': 'No tiene autorización para realizar esta acción'})
   ## Valida que se enviarion todos los campos
   campos = ['diccionario']
   valida = validateFiles(campos, request.files)
   if valida['response'] == 'ERROR':
      return jsonify(valida)
   ## Obtiene los archivos del request
   diccionario = request.files['diccionario']
   try:
      dicc = empresa.addDiccionario(diccionario, idCompany, niveles)
      return jsonify({'response': 'OK', 'data': dicc})
   except Exception:
      traceback.print_exc()
      return jsonify({'response': 'ERROR', 'message': 'Se presentó un error al procesar el archivo ' + diccionario.filename})

@app.route('/files/employes/<idCompany>', methods = ['POST'])
@privated
def loadEmployes(usuario, idCompany):
   '''
       loadEmployes: Recibe el archivo empleado de una empresa para procesarlos y guardarlos en la DB \n
       @params: 
         idCompany: Id mongo de la empresa
   '''
   print("In loadEmployes:", idCompany)
   if usuario['perfil'] == 'client':
      return jsonify({'response': 'ERROR', 'message': 'No tiene autorización para realizar esta acción'})
   ## Valida que se enviarion todos los campos
   campos = ['usuarios']
   valida = validateFiles(campos, request.files)
   if valida['response'] == 'ERROR':
      return jsonify(valida)
   ## Obtiene los archivos del request
   usuarios    = request.files['usuarios']
   try:
      usus = empresa.addEmpleados(usuarios, idCompany)
      return jsonify({'response': 'OK', 'data': usus})
   except Exception:
      traceback.print_exc()
      return jsonify({'response': 'ERROR', 'message': 'Se presentó un error al procesar el archivo ' + usuarios.filename})

@app.route('/files/frecuency/<idCompany>', methods = ['POST'])
@privated
def loadFrecuency(usuario, idCompany):
   '''
       loadFrecuency: Recibe el archivo frecuencias de una empresa para procesarlo y guardarlo en la DB \n
       @params: 
         idCompany: Id mongo de la empresa
   '''
   print("In loadFrecuency:", idCompany)
   if usuario['perfil'] == 'client':
      return jsonify({'response': 'ERROR', 'message': 'No tiene autorización para realizar esta acción'})
   ## Valida que se enviarion todos los campos
   campos = ['frecuencias']
   valida = validateFiles(campos, request.files)
   if valida['response'] == 'ERROR':
      return jsonify(valida)
   ## Obtiene los archivos del request
   frecuencias = request.files['frecuencias']
   try:
      frec = empresa.addFrecuacia(frecuencias, idCompany)
      return jsonify({'response': 'OK', 'data': frec})
   except Exception:
      traceback.print_exc()
      return jsonify({'response': 'ERROR', 'message': 'Se presentó un error al procesar el archivo ' + frecuencias.filename})

@app.route('/full/company/<idCompany>', methods = ['GET'])
@privated
def getCompanyFull(usuario, idCompany):
   '''
       getCompanyFull: Recupera todos los datos de una empresa junto con su diccionario, frecuecias y empleados \n
       @params: 
         idCompany: Id mongo de la empresa
   '''
   print("In getCompany:", idCompany)
   resp = empresa.getFullCompanyById(idCompany)
   return jsonify(resp)

@app.route('/full/dictionary/<idCompany>', methods = ['GET'])
@privated
def getDictionary(usuario, idCompany):
   '''
       getDictionary: Recupera todos los datos de una empresa junto con su diccionario \n
       @params: 
         idCompany: Id mongo de la empresa
   '''
   print("In getDictionary:", idCompany)
   resp = empresa.getDiccionarioByCompany(idCompany)
   return jsonify(resp)

@app.route('/full/frecuency/<idCompany>', methods = ['GET'])
@privated
def getFrecuency(usuario, idCompany):
   '''
       getFrecuency: Recupera todos los datos de una empresa junto con sus frecuencias \n
       @params: 
         idCompany: Id mongo de la empresa
   '''
   print("In getFrecuency:", idCompany)
   resp = empresa.getFrecuenciasByCompany(idCompany)
   return jsonify(resp)

@app.route('/full/employes/<idCompany>', methods = ['GET'])
@privated
def getEmployes(usuario, idCompany):
   '''
       getEmployes: Recupera todos los datos de una empresa junto con sus empleados \n
       @params: 
         idCompany: Id mongo de la empresa
   '''
   print("In getDictionary:", idCompany)
   if usuario['perfil'] == 'client':
      return jsonify({'response': 'ERROR', 'message': 'No tiene autorización para acceder a esta información'})
   resp = empresa.getEmpleadosByCompany(usuario, idCompany)
   return jsonify(resp)