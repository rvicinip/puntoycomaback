from src import db, ma

class Usuario(db.Model):
    id_usuario = db.Column(db.String(20), primary_key = True, nullable = False)
    nombre     = db.Column(db.String(200), nullable = False)
    empresa    = db.Column(db.Integer, nullable = False)
    clave      = db.Column(db.String(300), nullable = False)
    email      = db.Column(db.String(100))
    cargo      = db.Column(db.String(50))
    salario    = db.Column(db.Integer)
    jornada    = db.Column(db.String(10))
    perfil     = db.Column(db.String(10))
    ccostos    = db.Column(db.String(50))
    termino    = db.Column(db.String(10))
    estado     = db.Column(db.String(3))
    codigo     = db.Column(db.Integer)

    def __init__(self, id_usuario, clave, nombre, empresa, email, cargo, salario, jornada, perfil, ccostos, termino, estado, codigo):
        self.id_usuario = id_usuario
        self.nombre     = nombre
        self.empresa    = empresa
        self.clave      = clave
        self.email      = email
        self.cargo      = cargo
        self.salario    = salario
        self.jornada    = jornada
        self.perfil     = perfil
        self.ccostos    = ccostos
        self.termino    = termino
        self.estado     = estado
        self.codigo     = codigo
    
    def __init__(self, user):
        self.id_usuario = user['id_usuario']
        self.nombre     = user['nombre']
        self.empresa    = user['empresa']
        self.clave      = user['clave']
        self.email      = user['email']
        self.cargo      = user['cargo']
        self.salario    = user['salario']
        self.jornada    = user['jornada']
        self.perfil     = user['perfil']
        self.ccostos    = user['ccostos']
        self.termino    = user['termino']
        self.estado     = user['estado']
        self.codigo     = user['codigo']
    
    def toJSON(self):
        return {
            'id_usuario' : self.id_usuario,
            'nombre'     : self.nombre,
            'empresa'    : self.empresa,
            'clave'      : self.clave,
            'email'      : self.email,
            'cargo'      : self.cargo,
            'salario'    : self.salario,
            'jornada'    : self.jornada,
            'perfil'     : self.perfil,
            'ccostos'    : self.ccostos,
            'termino'    : self.termino,
            'estado'     : self.estado,
            'codigo'     : self.codigo}

class usuarioScheme(ma.Schema):
    class Meta:
        fields = (
            'id_usuario', 
            'clave', 
            'nombre', 
            'empresa', 
            'email', 
            'cargo', 
            'salario', 
            'jornada', 
            'perfil', 
            'ccostos', 
            'termino', 
            'estado',
            'codigo')

usuario   = usuarioScheme()
usuarios  = usuarioScheme(many=True)