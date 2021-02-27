'''
   validator:
     Realiza las diferentes validaciones necesarias para el desarrollo

   copyright 2021 - Vitt Inversiones SAS - vitt.co
   license:
     by Vitt Inversiones SAS - vitt.co
   author: Wiliam Arévalo Camacho
'''
### Se importan los plugins necesarios
import re

def validateExcel(name):
   '''
       validateExcel: Verifica que el archivo si sea un archivo Excel \n
       @params: 
         name: Nombre del archivo a validar
   '''
   print("In validateExcel")
   excel = set(['xls', 'xlsm'])
   return validateFileType(name, excel)

def validateFileType(name, type):
   '''
       validateFileType: Verifica que un archivo sea de un tipo específico \n
       @params: 
         name: Nombre del archivo a valida
         type: Extenciones permitidas para el archivo
   '''
   print("In validateFileType")
   ext = name.rsplit(".")[-1].lower()
   if "." in name and ext in type:
      return True
   return False

def validateEmail(email):
   '''
       validateEmail: Verifica que un email este bien escrito \n
       @params: 
         email: dirección de email a validar
   '''
   print("validateEmail")
   regexp = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
   return re.match(regexp, email) is not None

def validateFields(fields, data):
   '''
       validateFileType: Verifica que un archivo sea de un tipo específico \n
       @params: 
         fields: Lista de campos que se deben validar
         data: Datos a validar
   '''
   print("In validateFields")
   for value in fields:
      if not value in data:
         return {'response':'ERROR', 'message': value + ' es requerido, por favor verifíque'}
      if not data[value]:
         return {'response':'ERROR', 'message': value + ' es obligatorio, por favor verifíque'}
   return {'response': 'OK', 'message': 'Todas las validaciones realizadas'}

def validateFiles(fields, files):
   '''
       validateFileType: Verifica que un archivo sea de un tipo específico \n
       @params: 
         fields: Lista de campos que se deben validar
         data: Datos a validar
   '''
   print("In validateFiles" + fields)
   for value in fields:
      if not value in files:
         return {'response':'ERROR', 'message': 'No se recibió el archivo de ' + value + ', por favor verifíque'}
      if files[value].filename == '':
         return {'response':'ERROR', 'message': 'No se seleccionó el archivo de ' + value + ', por favor verifíque'}
      if not validateExcel(files[value].filename):
         return {'response': 'ERROR', 'message': 'El archivo ' + value + ' no es de tipo Excel'}
   return {'response': 'OK', 'message': 'Todas las validaciones realizadas'}

def codeTransform(field):
   '''
      codeTransform: transforma el código en el evento que tenga ',' y transforma el código '0' adelante
      @Params:
         field: Campo a validar 
   '''
   print('In codeTransform:', field)
   value = str(field)
   if not value or value.lower() == 'nan' or value == '0.0':
      return str(0)
   if ',' in value:
      value = str(value).replace(',', '.')
   code = value.split('.')
   resp = ''
   for c in code:
      if int(c) > 0:
         ln = 3 - len(c)
         if ln > 0:
            resp = str(resp) + str(ln * '0' + str(c))
         elif ln == 0:
            resp += c
         else:
            resp += str(c[-3:ln])
   print('Transformed:', resp)
   return resp