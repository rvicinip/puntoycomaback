'''
   connector

   Método generico de acceso a una base de datos en MongoDB definiendo los métodos genrales del CRUD (Create, Read, Update, Delete)

   copyright 2021 - Vitt Inversiones SAS - vitt.co
   licensed by Vitt Inversiones SAS - vitt.co
   author: Wiliam Arévalo Camacho
'''
### Se importan los plugins necesarios
from bson import ObjectId
from pymongo import MongoClient
from src.mongoCRUD import parsser
import traceback

def addToCollection(url, dbName, collection, values):
  '''
     addToCollection: Agrega un registro en una colección de la DB \n
     @params: 
       url: ruta de conxión a la DB
       dbName: Nombre de la DB a la  que se conectará
       collection: Nombre de la colección en la que se buscarán los datos
       values: objeto Json con los datos a insertar en la DB 
  '''
  print("In addToCollection:", collection)
  try:
    client = MongoClient(url)
    db     = client[dbName]
    mdb    = db[collection]
    res    = mdb.insert(values)
    resp   = str(ObjectId(res))
    client.close()
    return resp
  except Exception:
    traceback.print_exc()
    return {'ERROR': 'Se presentó un error al crear un registro en ' + collection}

def getCollectionById(url, dbName, collection, idMongo):
  '''
     getCollectionById: Busca un registro en una colección por el id de mongo '_id' \n
     @params: 
       url: ruta de conxión a la DB
       dbName: Nombre de la DB a la  que se conectará
       collection: Nombre de la colección en la que se buscarán los datos
       idMongo: Id del objeto a buscar en la DB 
  '''
  print("In getCollectionById:", collection)
  try:
    client = MongoClient(url)
    db     = client[dbName]
    mdb    = db[collection]
    res    = mdb.find_one({'_id': ObjectId(idMongo)})
    if res != None:
      resp = parsser.parserObjectId(res)
    else:
      resp = {'ERROR': 'NO se encontró ' + idMongo}
    client.close()
    return resp
  except Exception:
    traceback.print_exc()
    return {'ERROR': 'Se presentó un error al consultar en ' + collection}

def getCollecctionByField(url, dbName, collection, field):
  '''
     getCollecctionByField: Busca un único registro en la coleeción acorde con un campo en partícular \n
     @params: 
       url: ruta de conxión a la DB
       dbName: Nombre de la DB a la  que se conectará
       collection: Nombre de la colección en la que se buscarán los datos
       field: Objeto Json con el campo y el valor a buscar en la DB
  '''
  print("In getCollecctionByField:", collection)
  try:
    client = MongoClient(url)
    db     = client[dbName]
    mdb    = db[collection]
    res    = mdb.find_one(field)
    if res != None:
      resp   = parsser.parserObjectId(res)
    else:
      resp = {'ERROR': 'NO se encontraron resultados'}
    client.close()
    return resp
  except Exception:
    traceback.print_exc()
    return {'ERROR': 'Se presentó un error al consultar en ' + collection }

def getCollecctionsByField(url, dbName, collection,field):
  ''' 
     :getCollecctionsByField: Busca todos los registros en una colección acorde a un campo \n
     @params: 
       url: ruta de conxión a la DB
       dbName: Nombre de la DB a la  que se conectará
       collection: Nombre de la colección en la que se buscarán los datos
       field: Objeto Json con los valores a buscar en la DB
  '''
  print("In getCollecctionsByField:", collection)
  try:
    resp = []
    client = MongoClient(url)
    db     = client[dbName]
    mdb    = db[collection]
    result = mdb.find(field)
    print(result)
    if result != None:
      for dato in result:
        resp.append(parsser.parserObjectId(dato))
    client.close()
    return resp
  except Exception:
    traceback.print_exc()
    return {'ERROR': 'Se presentó un error al consultar en ' + collection}

def getAllInCollecction(url, dbName, collection):
  '''
     getAllInCollecction: Busca todos los registros en una colección \n
     @params: 
       url: ruta de conxión a la DB
       dbName: Nombre de la DB a la  que se conectará
       collection: Nombre de la colección en la que se buscarán los datos
  '''
  print("In getAllInCollecction:", collection)
  try:
    resp = []
    client = MongoClient(url)
    db     = client[dbName]
    mdb    = db[collection]
    result = mdb.find()
    if result != None:
      for dato in result:
        resp.append(parsser.parserObjectId(dato))
    client.close()
    return resp
  except Exception:
    traceback.print_exc()
    return {'ERROR': 'Se presentó un error al consultar en ' + collection}

def deleteById(url, dbName, collection, idMongo):
  '''
     deleteById: Elimina un registro en la colección \n
     @params: 
       url: ruta de conxión a la DB
       dbName: Nombre de la DB a la  que se conectará
       collection: Nombre de la colección en la que se buscarán los datos
       idMongo: Id del objeto a eliminar de la DB
  '''
  print("In deleteById:", collection)
  try:
    client = MongoClient(url)
    db     = client[dbName]
    mdb    = db[collection]
    resp = mdb.delete_one({'_id': ObjectId(idMongo)})
    client.close()
    return resp
  except Exception:
    traceback.print_exc()
    return {'ERROR': 'Se presentó un error al eliminar un registro en ' + collection}

def updateById(url, dbName, collection, objeto):
  '''
     updateById: Actualiza un registro en la colección \n
     @params: 
       url: ruta de conxión a la DB
       dbName: Nombre de la DB a la  que se conectará
       collection: Nombre de la colección en la que se buscarán los datos
       objeto: Objeto con los datos a actualizar
  '''
  print("In updateUById:", collection)
  try:
    valores = parsser.removeObjectId(objeto)
    client = MongoClient(url)
    db     = client[dbName]
    mdb    = db[collection]
    resp = mdb.update_one({'_id': ObjectId(objeto['_id'])}, {"$set": valores})
    client.close()
    return resp
  except Exception:
    traceback.print_exc()
    return {'ERROR': 'Se presentó un error al modificar la colección ' + collection}
