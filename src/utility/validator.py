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
   excel = set(['xls', 'xlsm'])
   return validateFileType(name, excel)

def validateFileType(name, type):
   '''
       validateFileType: Verifica que un archivo sea de un tipo específico \n
       @params: 
         name: Nombre del archivo a valida
         type: Extenciones permitidas para el archivo
   '''
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
   regexp = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
   return re.match(regexp, email) is not None
