'''
   xlsReader:
     transforma el contenido de un archivo xls en un Json

   copyright 2021 - Vitt Inversiones SAS - vitt.co
   license:
     by Vitt Inversiones SAS - vitt.co
   author: Wiliam Arévalo Camacho
'''
### Se importan los plugins necesarios
import pandas as xls
import traceback

def readXLS(document, hoja):
  '''
     readXLS: Transdorma un libro de Excel en una lista de objetos Json \n
     @params: 
       document: Aechivo a procesar
       hoja: Número de la hoja a procesar
  '''
  print("In readXLS")
  try:
    arch  = xls.ExcelFile(document)
    hojas = arch.sheet_names
    data = arch.parse(hojas[hoja-1])
    resp = []
    for index, row in data.iterrows():
      reg = {}
      for t in range(len(data.columns)):
        val = row[data.columns[t]]
        if str(val).lower() == 'nan':
          val = None
        reg[str(data.columns[t]).lower()] = val
      resp.append(reg)
    return resp
  except Exception:
    traceback.print_exc()
    return {'ERROR': 'Se presentó un error leyendo el archivo ' + document.filename}

def validateXLS(hoja, fields):
  '''
     validateXLS: Verifica que la información extraida de un libro de Excel contenga los campos solicitados \n
     @params: 
       hoja: Contiene la información obtenida del archivo Excel
       fields: Lista de los campos que se desean validar en el archivo
  '''
  print("In validateXLS")
  try:
    resp = []
    for data in hoja:
      ind = True
      c = 0
      while c < len(fields) and ind:
        if str(data[fields[c]]).lower() == 'nan':
          ind = False
          resp.append(data)
        c += 1
    if len(resp) > 0:
      return {'ERROR': 'Existen algunos registros que no tienen toda la información solicitada', 'data': resp}
    return {'OK': 'Todos los registros tiene los campos solicitados'}
  except Exception:
    traceback.print_exc()
    return {'ERROR': 'Se presentó un error validando los campos ' + fields}  