from src import db, ma

class Diccionario(db.Model):
    id              = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement=True)
    id_actividad    = db.Column(db.String(15), nullable = False)
    nombre          = db.Column(db.String(200), nullable = False)
    empresa         = db.Column(db.Integer, nullable = False)
    nivel           = db.Column(db.Integer, nullable = False)
    padre           = db.Column(db.String(15))
    descripcion     = db.Column(db.String(300))
    mas             = db.Column(db.String(20))
    ceno            = db.Column(db.String(20))
    tipo            = db.Column(db.String(20))
    cadena_de_valor = db.Column(db.String(20))

    def __init__(self, id, id_actividad, nombre, empresa, nivel, padre, descripcion, mas, ceno, tipo, cadena_de_valor):
        self.id              = id
        self.id_actividad    = id_actividad
        self.nombre          = nombre
        self.empresa         = empresa
        self.nivel           = nivel
        self.padre           = padre
        self.descripcion     = descripcion
        self.mas             = mas
        self.ceno            = ceno
        self.tipo            = tipo
        self.cadena_de_valor = cadena_de_valor
    
    def __init__(self, dicc):
        self.id              = dicc['id']
        self.id_actividad    = dicc['id_actividad']
        self.nombre          = dicc['nombre']
        self.empresa         = dicc['empresa']
        self.nivel           = dicc['nivel']
        self.padre           = dicc['padre']
        self.descripcion     = dicc['descripcion']
        self.mas             = dicc['mas']
        self.ceno            = dicc['ceno']
        self.tipo            = dicc['tipo']
        self.cadena_de_valor = dicc['cadena_de_valor']
    
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