'''
   empresa:
      Modelo de datos de la entidad empresa en la DB MySQL

   copyright 2021 - Vitt Inversiones SAS - vitt.co:
      licensed to Velasquez Naranjo y Cia SAS - Venaycia.com
   author: Wiliam Arévalo Camacho
'''
from src import db, ma

class Empresa(db.Model):
    nit     = db.Column(db.String(20), primary_key = True, nullable = False)
    nombre  = db.Column(db.String(200), nullable = False)
    niveles = db.Column(db.Integer, nullable = False)
    estado  = db.Column(db.String(3), nullable = False)
    tipo    = db.Column(db.String(10))
    
    def __init__(self, nit, nombre, niveles, tipo,  estado):
        self.nit     = nit
        self.nombre  = nombre
        self.niveles = niveles
        self.tipo    = tipo
        self.estado  = estado
    
    def __init__(self, emp):
        self.nit     = emp['nit']
        self.nombre  = emp['nombre']
        self.niveles = emp['niveles']
        self.tipo    = emp['tipo'] if ('tipo' in emp) else 'Client'
        self.estado  = emp['estado'] if ('estado' in emp) else 'A'     ## valor_si if condicion else valor_no
    
    def toJSON(self):
        return {
            'nit'     : self.nit,
            'nombre'  : self.nombre,
            'niveles' : self.niveles,
            'estado'  : self.estado,
            'tipo'    : self.tipo}

class empresaScheme(ma.Schema):
    class Meta:
        fields = (
            'nit', 
            'nombre', 
            'niveles', 
            'tipo', 
            'estado')

empresa   = empresaScheme()
empresas  = empresaScheme(many=True)