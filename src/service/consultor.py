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
from .protector import privated

@app.route('/consultor/<company>/<user>', methods = ['POST'])
@privated
def addCompaniesConsultor(usuario, company, user):
    '''
        addCompaniesConsultor: Asocia una empresas a un consultor \n
        @params:
          :company: Nit de la empreesa a asociar
          :user: id_usuario del consultar a asociar con la empresa
    '''
    print("In addCompaniesConsultor")   
    if usuario['perfil'] != 'consult':
       return {'response': 'ERROR', 'message': 'No tiene los privilegios de consultor, no puede realizar esta acción'}
    resp = consultor.asociateCompany(company, user)
    return jsonify(resp)

@app.route('/consultor', methods = ['GET'])
@privated
def getCompaniesConsultor(usuario):
   '''
       getCompaniesConsultor: Recupera todas las empresas asociadas al usuario en login \n
   '''
   print("In getCompaniesConsultor")    
   resp = consultor.getCompaniesConsultor(usuario['id_usuario'])
   return jsonify(resp)
