from src import db, ma

class Frecuencia(db.Model):
    id      = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement = True)
    nombre  = db.Column(db.String(200), nullable = False)
    tipo    = db.Column(db.Integer, nullable = False)
    valor   = db.Column(db.Float, nullable = False)
    empresa = db.Column(db.String(20), nullable = False)
    unidad  = db.Column(db.String(15))

    def __init__(self, nombre, tipo, valor, empresa, unidad):
        self.nombre  = nombre
        self.empresa = empresa
        self.tipo    = tipo
        self.valor   = valor
        self.unidad  = unidad
    
    def __init__(self, frec):
        self.nombre  = frec['nombre']
        self.empresa = frec['empresa']
        self.tipo    = frec['tipo']
        self.valor   = frec['valor']
        self.unidad  = (None, frec['unidad'])['unidad' in frec]  ## Ternario (ValorSiFalso, ValorSiVerdadero)[Condición]
    
    def toJSON(self):
        return {
            'id'      : self.id,
            'nombre'  : self.nombre,
            'empresa' : self.empresa,
            'tipo'    : self.tipo,
            'valor'   : self.valor,
            'unidad'  : self.unidad}
    
class frecuenciaScheme(ma.Schema):
    class Meta:
        fields = (
            'id', 
            'nombre', 
            'empresa', 
            'tipo', 
            'valor', 
            'unidad')

frecuencia  = frecuenciaScheme()
frecuencias = frecuenciaScheme(many=True)