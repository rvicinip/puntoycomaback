'''
   diccionario:
      Modelo de datos de la entidad diccionario en la DB MySQL

   copyright 2021 - Vitt Inversiones SAS - vitt.co:
      licensed to Velasquez Naranjo y Cia SAS - Venaycia.com
   author: Wiliam Arévalo Camacho
'''
from src import db, ma

class Diccionario(db.Model):
    id              = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement=True)
    id_actividad    = db.Column(db.String(15), nullable = False)
    nombre          = db.Column(db.String(200), nullable = False)
    empresa         = db.Column(db.String(20), nullable = False)
    nivel           = db.Column(db.Integer, nullable = False)
    padre           = db.Column(db.String(15))
    id_padre        = db.Column(db.Integer)
    descripcion     = db.Column(db.String(400))
    mas             = db.Column(db.String(20))
    ceno            = db.Column(db.String(20))
    tipo            = db.Column(db.String(20))
    cadena_de_valor = db.Column(db.String(20))

    def __init__(self, id_actividad, nombre, empresa, nivel, padre, id_padre, descripcion, mas, ceno, tipo, cadena_de_valor):
        self.id_actividad    = id_actividad
        self.nombre          = nombre
        self.empresa         = empresa
        self.nivel           = nivel
        self.padre           = padre
        self.id_padre        = id_padre
        self.descripcion     = descripcion
        self.mas             = mas
        self.ceno            = ceno
        self.tipo            = tipo
        self.cadena_de_valor = cadena_de_valor
    
    def __init__(self, dicc):
        self.id_actividad    = str(dicc['id_actividad'])
        self.nombre          = dicc['nombre']
        self.empresa         = dicc['empresa']
        self.nivel           = dicc['nivel']
        self.padre           = str(dicc['padre']) if ('padre' in dicc) else '0'
        self.id_padre        = dicc['id_padre'] if ('id_padre' in dicc) else None
        self.descripcion     = dicc['descripcion'] if ('descripcion' in dicc) else None
        self.mas             = dicc['mas'] if ('mas' in dicc) else None
        self.ceno            = dicc['ceno'] if ('ceno' in dicc) else None
        self.tipo            = dicc['tipo'] if ('tipo' in dicc) else None
        self.cadena_de_valor = dicc['cadena_de_valor'] if ('cadena_de_valor' in dicc) else None     ## Ternario valor_si if condicion else valor_no
    
    def toJSON(self):
        return{
            'id'              : self.id,
            'id_actividad'    : self.id_actividad,
            'nombre'          : self.nombre,
            'empresa'         : self.empresa,
            'nivel'           : self.nivel,
            'padre'           : self.padre,
            'descripcion'     : self.descripcion,
            'mas'             : self.mas,
            'ceno'            : self.ceno,
            'tipo'            : self.tipo,
            'cadena_de_valor' : self.cadena_de_valor}

class diccionarioScheme(ma.Schema):
    class Meta:
        fields = (
            'id',
            'id_actividad',
            'nombre', 
            'empresa', 
            'nivel', 
            'padre', 
            'descripcion', 
            'mas', 
            'ceno', 
            'tipo', 
            'cadena_de_valor')

diccionario  = diccionarioScheme()
diccionarios = diccionarioScheme(many=True)