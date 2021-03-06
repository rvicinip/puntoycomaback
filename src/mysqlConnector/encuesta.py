'''
   encuesta:
      Modelo de datos de la entidad encuesta en la DB MySQL

   copyright 2021 - Vitt Inversiones SAS - vitt.co:
      licensed to Velasquez Naranjo y Cia SAS - Venaycia.com
   author: Wiliam Arévalo Camacho
'''
from src import db, ma

class Encuesta(db.Model):
    id         = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement=True)
    usuario    = db.Column(db.Integer, nullable = False)
    actividad  = db.Column(db.Integer, nullable = False)
    cantidad   = db.Column(db.Integer, nullable = False)
    tiempo     = db.Column(db.Float)
    umedida    = db.Column(db.Integer)
    frecuencia = db.Column(db.Integer)
    jornada    = db.Column(db.Float)
    fteAct     = db.Column(db.Float)
    fteUser    = db.Column(db.Float)
    valorAct   = db.Column(db.Integer)
    estado     = db.Column(db.String(3))

    def __init__(self, id, actividad, usuario, cantidad, tiempo, umedida, frecuencia, jornada, fteAct, fteUser, valorAct, estado):
        self.actividad  = actividad
        self.usuario    = usuario
        self.cantidad   = cantidad
        self.tiempo     = tiempo
        self.umedida    = umedida
        self.frecuencia = frecuencia
        self.jornada    = jornada
        self.fteAct     = fteAct
        self.fteUser    = fteUser
        self.valorAct   = valorAct
        self.estado     = estado
    
    def __init__(self, enc):
        self.actividad  = enc['actividad']
        self.usuario    = enc['usuario']
        self.cantidad   = enc['cantidad']
        self.tiempo     = enc['tiempo']     if ('tiempo' in enc)      else None 
        self.umedida    = enc['umedida']    if ('umedida' in enc)     else None 
        self.frecuencia = enc['frecuencia'] if ('frecuencia' in enc)  else None 
        self.jornada    = enc['jornada']    if ('jornada' in enc)     else None 
        self.fteAct     = enc['fteAct']     if ('fteAct' in enc)      else None 
        self.fteUser    = enc['FteUser']    if ('FteUser' in enc)     else None 
        self.valorAct   = enc['valorAct']   if ('valorAct' in enc)    else None 
        self.estado     = enc['estado']     if ('estado' in enc)      else 'A'      ## Ternario valor_si if condicion else valor_no
    
    def toJSON(self):
        return{
            'id'         : self.id,
            'actividad'  : self.actividad,
            'usuario'    : self.usuario,
            'cantidad'   : self.cantidad,
            'tiempo'     : self.tiempo,
            'umedida'    : self.umedida,
            'frecuencia' : self.frecuencia,
            'jornada'    : self.jornada,
            'fteAct'     : self.fteAct,
            'FteUser'    : self.fteUser,
            'valorAct'   : self.valorAct,
            'estado'     : self.estado}
    
class encuestaScheme(ma.Schema):
    class Meta:
        fields = (
            'id',
            'actividad',
            'usuario',
            'cantidad',
            'tiempo',
            'umedida',
            'frecuencia',
            'jornada',
            'fteAct',
            'fteUser',
            'valorAct',
            'estado')

encuesta   = encuestaScheme()
encuestas  = encuestaScheme(many=True)