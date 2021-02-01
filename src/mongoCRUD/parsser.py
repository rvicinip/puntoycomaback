'''
   parsser

   Realiza la tranformación de objetos no serializables a serializable, particularmente retirando el campo de tipo ObjectId de MongoDB\n

   copyright 2021 - Vitt Inversiones SAS - vitt.co \n
   licensed by Vitt Inversiones SAS - vitt.co \n
   author: Wiliam Arévalo Camacho
'''
### Se importan los plugins necesarios
from bson import ObjectId
import traceback

### Método de tranfosrmación del cursor a diccionario
def parserObjectId(data):
    '''
       parserObjectId: transforma un cursor de mongo en un diccionario \n
       @params: 
         cursorWithIdObject: cursor que posee un ObjectId de Mongo  
    '''
    print("In parserObjectId:", data)
    element = {}
    try:
      for c in data:
        if c == '_id':
          element[c] = str(ObjectId(data[c]))
        else:
          element[c] = data[c]
      return element
    except Exception:
      traceback.print_exc()
      return 

### Método de tranfosrmación del cursor a diccionario
def removeObjectId(data):
    '''
       removeObjectId: Retira de un diccionario el campo _id para la actualización \n
       @params: 
         data: cursor que posee un ObjectId de Mongo  
    '''
    print("In removeObjectId:", data)
    element = {}
    try:
      for c in data:
        if c != '_id':
          element[c] = data[c]
      return element
    except Exception:

      traceback.print_exc()
      return