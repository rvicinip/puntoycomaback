'''
   consultor:
      Modelo de datos de la entidad consultor en la DB MySQL

   copyright 2021 - Vitt Inversiones SAS - vitt.co:
      licensed to Velasquez Naranjo y Cia SAS - Venaycia.com
   author: Wiliam Arévalo Camacho
'''
from src import db, ma

class Consultor(db.Model):
    id        = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement = True)
    empresa   = db.Column(db.Integer, nullable = False)
    consultor = db.Column(db.Integer, nullable = False)
    estado    = db.Column(db.String(3), nullable = False)
    
    def __init__(self, empresa, consultor, estado):
        self.empresa   = empresa
        self.consultor = consultor
        self.estado    = estado
    
    def __init__(self, cons):
        self.id        = cons['id']
        self.empresa   = cons['empresa']
        self.consultor = cons['consultor'] 
        self.estado    = cons['estado'] if ('estado' in cons) else 'A'  ## valor_si if condicion else valor_no
    
    def toJSON(self):
        return{
            'id'        : self.id,
            'empresa'   : self.empresa,
            'consultor' : self.consultor,
            'estado'    : self.estado}

class consultorScheme(ma.Schema):
    class Meta:
        fields = (
            'id', 
            'empresa', 
            'consultor',  
            'estado')

consultor   = consultorScheme()
consultores = consultorScheme(many=True)