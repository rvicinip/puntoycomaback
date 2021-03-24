'''
   consultor:
      Administra los accesos a datos de los consultores de Venaycia.com 

   copyright 2021 - Vitt Inversiones SAS - vitt.co:
      licensed to Velasquez Naranjo y Cia SAS - Venaycia.com
   author: Wiliam Arévalo Camacho
'''
from src.mysqlConnector.consultor import Consultor
from src.model import empresa
from src.model import user
from src import db
import traceback

# Métodos CRUD en las coleeciones diccionario, empresa y frecuencias
### CREA
def asociateCompany(emp, cons):
  '''
     asociateCompany: Asocia una empresa a un consultor \n
     @params: 
       emp: Nit de la empresa a asociar
       cons: id_usuario del consultor a asociar
  '''
  print("In asociateCompany:", emp)
  try:
    valida = isConsultorInCompany(cons, emp)
    if 'data' in valida:
      estado = valida['data']['estado']
      estado = 'Activo' if estado == 'A' else 'Inactivo'
      return {'response': 'ERROR', 'message': 'El consultor se encuentra ' + estado + ' en la empresa ' + emp}  
    veriEmp = empresa.getCompanyByNIT(emp)
    if not 'data' in veriEmp:
      return {'response': 'ERROR', 'message': 'No existe la empresa con el NIT ' + str(emp)}  
    veriCons = user.getUserByUsuario(cons)
    if not 'data' in veriCons:
      return {'response': 'ERROR', 'message': 'No existe el consultor con el Id de usuario ' + str(cons)}
    perfil = veriCons['data']['perfil']
    if perfil != 'consult':
      return {'response': 'ERROR', 'message': 'No se puede asociar el usuario ' + str(cons) + ' a la empresa ' + str(emp) + ' no tiene los privilegios de consultor'}
    c = Consultor(emp, cons, 'A')
    db.session.add(c)
    db.session.commit()
    return {'response': 'OK', 'message': 'Consultor asociado a la empresa '+ str(emp), 'data': c.toJSON()}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error al asociar el usuario ' + str(cons)}

### LEE
def getCompaniesConsultor(idCons):
  '''
     getCompaniesConsultor: Busca todas las empresas en DB \n
     @params: 
       cons: id_usuario del consultor a buscar
  '''
  print("In getCompaniesConsultor")
  try:
    usu = user.getUserByUsuario(idCons)
    if not 'data' in usu:
        return usu
    consultor = usu['data']
    if not consultor['perfil'] == 'consult':
      return {'response': 'ERROR', 'message': 'El usuario no tiene privilegios de consultor'}
    resp = []
    emps = Consultor.query.filter(Consultor.consultor == idCons, Consultor.estado == 'A')
    for e in emps:
      con = e.toJSON()
      emp = empresa.getCompanyByNIT(e.empresa)
      if 'data' in emp:
        c = emp['data']
        con['nit']     = c['nit']
        con['nombre']  = c['nombre']
        con['usuario'] = consultor['nombre']
        resp.append(con)
    if len(resp) > 0:
      return {'response': 'OK', 'data': resp}
    return {'response': 'ERROR', 'message': 'No se encontraron empresas para el consultor ' + str(idCons)}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error al consultar las empresas'}

def isConsultorInCompany(idCons, idEmpr):
  '''
     isConsultorInCompany: Busca si una empresa está asociada a un consultor en la DB \n
     @params: 
       idCons: id_usuario del consultor a buscar
       idEmpr: nit de la empresa cliente
  '''
  print("In isConsultorInCompany")
  try:
    resp = Consultor.query.filter(Consultor.consultor == idCons, Consultor.empresa == idEmpr).first()
    if resp:
      return {'response': 'OK', 'data': resp.toJSON()}
    return {'response': 'ERROR', 'message': 'El consultor no se encuentra asociado a esta empresa'}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error al consultar las empresas'}

### ACTUALIZA
def removeConsultor(emp, cons):
  '''
     removeConsultor: Asocia una empresa a un consultor \n
     @params: 
       emp: Nit de la empresa a asociar
       cons: id_usuario del consultor a eleminar
  '''
  print("In removeConsultor:", emp)
  try:
    veriEmp = empresa.getCompanyByNIT(emp)
    if not 'data' in veriEmp:
      return {'response': 'ERROR', 'message': 'No existe la empresa con el NIT ' + emp}  
    veriCons = user.getUserByUsuario(cons)
    if not 'data' in veriCons:
      return {'response': 'ERROR', 'message': 'No existe el consultor con el Id de usuario ' + cons}
    c = Consultor.query.filter(Consultor.empresa == emp, Consultor.consultor == cons).update({
                                 Consultor.estado : 'D'})
    db.session.commit()
    return {'response': 'OK', 'message': 'Consultor eliminado de la empresa '+ emp}
  except Exception:
    traceback.print_exc()
    return {'response': 'ERROR', 'message': 'Se presentó un error al asociar el usuario ' + cons}
