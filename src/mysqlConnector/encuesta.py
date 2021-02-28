from src import db, ma

class Encuesta(db.Model):
    id         = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement=True)
    usuario    = db.Column(db.Integer, nullable = False)
    actividad  = db.Column(db.Integer, nullable = False)
    cantidad   = db.Column(db.Integer, nullable = False)
    tiempo     = db.Column(db.Float, nullable = False)
    umedida    = db.Column(db.Integer, nullable = False)
    frecuencia = db.Column(db.Integer, nullable = False)
    jornada    = db.Column(db.Float)
    fteAct     = db.Column(db.Float)
    fteUser    = db.Column(db.Float)
    valorAct   = db.Column(db.Integer)
    estado     = db.Column(db.String(3))

    def __init__(self, id, actividad, usuario, cantidad, tiempo, umedida, frecuencia, jornada, fteAct, fteUser, valorAct, estado):
        self.id         = id
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
        self.id         = enc['id']
        self.actividad  = enc['actividad']
        self.usuario    = enc['usuario']
        self.cantidad   = enc['cantidad']
        self.tiempo     = enc['tiempo']
        self.umedida    = enc['umedida']
        self.frecuencia = enc['frecuencia']
        self.jornada    = (None, enc['jornada'])['jornada' in enc]
        self.fteAct     = (None, enc['fteAct'])['fteAct' in enc]
        self.fteUser    = (None, enc['FteUser'])['FteUser' in enc]
        self.valorAct   = (None, enc['valorAct'])['valorAct' in enc]
        self.estado     = (None, enc['estado'])['estado' in enc]        ## Ternario (ValorSiFalso, ValorSiVerdadero)[Condición]
    
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