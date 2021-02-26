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
    
    def fromJSON(self, emp):
        self.nit     = emp['id']
        self.nombre  = emp['actividad']
        self.niveles = emp['usuario']
        self.tipo    = emp['cantidad']
        self.estado  = emp['tiempo']

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