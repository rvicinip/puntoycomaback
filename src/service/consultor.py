'''
   consultor:
      Administra los servicios de los consultores de las empresas clientes de Venaycia.com 

   copyright 2021 - Vitt Inversiones SAS - vitt.co:
      licensed to Velasquez Naranjo y Cia SAS - Venaycia.com
   author: Wiliam Arévalo Camacho
'''
from src.model import consultor
from flask import jsonify, request
from src import app
from src.utility import validator
from .protector import privated

@app.route('/consultor', methods = ['POST'])
@privated
def addCompaniesConsultor(usuario):
    '''
        addCompaniesConsultor: Asocia una empresas a un consultor \n
    '''
    print("In addCompaniesConsultor")
    dato = request.json
    campos = ['empresa', 'id_usuario']
    valida = validator.validateFields(campos, dato)
    if valida['response'] == 'ERROR':
      return jsonify(valida)
    if usuario['perfil'] != 'consult':
       return jsonify({'response': 'ERROR', 'message': 'No tiene los privilegios de consultor, no puede realizar esta acción'})
    resp = consultor.asociateCompany(dato['nit'], dato['id_usuario'])
    print("End addCompaniesConsultor:", resp)
    return jsonify(resp)

@app.route('/consultor/<company>/<user>', methods = ['DELETE'])
@privated
def deleteConsultor(usuario, company, user):
    '''
        deleteConsultor: Remueve un consultor de una empresas \n
        @params:
          :company: Nit de la empreesa
          :user: id_usuario del consultar a remover de la empresa
    '''
    print("In deleteConsultor")
    
    if usuario['perfil'] != 'consult':
       return {'response': 'ERROR', 'message': 'No tiene los privilegios de consultor, no puede realizar esta acción'}
    resp = consultor.removeConsultor(company, user)
    print("End deleteConsultor:", resp)
    return jsonify(resp)

@app.route('/consultor', methods = ['GET'])
@privated
def getCompaniesConsultor(usuario):
   '''
       getCompaniesConsultor: Recupera todas las empresas asociadas al usuario en login \n
   '''
   print("In getCompaniesConsultor")
   resp = consultor.getCompaniesConsultor(usuario['id_usuario'])
   print("End getCompaniesConsultor:", resp)
   return jsonify(resp)

@app.route('/consultors/<company>', methods = ['GET'])
@privated
def getConsultors(usuario, company):
    '''
        getConsultors: Trae los consultores asociados a una empresas \n
        @params:
          :company: Nit de la empreesa
    '''
    print("In getConsultors")
    
    if usuario['perfil'] != 'director':
       return {'response': 'ERROR', 'message': 'No tiene los privilegios para realizar esta acción'}
    resp = consultor.getConsultorsCompany(company)
    print("End getConsultors:", resp)
    return jsonify(resp)
