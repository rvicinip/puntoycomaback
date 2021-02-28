from src import db, ma

class Usuario(db.Model):
    id_usuario     = db.Column(db.String(20), primary_key = True, nullable = False)
    nombre         = db.Column(db.String(200), nullable = False)
    empresa        = db.Column(db.String(20), nullable = False)
    clave          = db.Column(db.String(255), nullable = False)
    email          = db.Column(db.String(100))
    cargo          = db.Column(db.String(50))
    salario        = db.Column(db.Integer)
    jornada        = db.Column(db.String(10))
    perfil         = db.Column(db.String(10))
    centrocosto    = db.Column(db.String(50))
    tipocontrato   = db.Column(db.String(10))
    estado         = db.Column(db.String(3))
    codigo         = db.Column(db.Integer)
    estadoEncuesta = db.Column(db.String(3))

    def __init__(self, id_usuario, clave, nombre, empresa, email, cargo, salario, jornada, perfil, centrocosto, tipocontrato, estado, codigo, estadoEncuesta):
        self.id_usuario     = id_usuario
        self.nombre         = nombre
        self.empresa        = empresa
        self.clave          = clave
        self.email          = email
        self.cargo          = cargo
        self.salario        = salario
        self.jornada        = jornada
        self.perfil         = perfil
        self.centrocosto    = centrocosto
        self.tipocontrato   = tipocontrato
        self.estado         = estado
        self.codigo         = codigo
        self.estadoEncuesta = estadoEncuesta
    
    def __init__(self, user):
        self.id_usuario     = user['id_usuario']
        self.nombre         = user['nombre']
        self.empresa        = user['empresa']
        self.clave          = user['clave']
        self.email          = (None, user['email'])['email' in user]
        self.cargo          = (None, user['cargo'])['cargo' in user]
        self.salario        = (None, user['salario'])['salario' in user]
        self.jornada        = (None, user['jornada'])['jornada' in user]
        self.perfil         = (None, user['perfil'])['perfil' in user]
        self.centrocosto    = (None, user['centrocosto'])['centrocosto' in user]
        self.tipocontrato   = (None, user['tipocontrato'])['tipocontrato' in user]
        self.estado         = ('A', user['estado'])['estado' in user]
        self.codigo         = (0, user['codigo'])['codigo' in user]
        self.estadoEncuesta = ('P', user['estadoEncuesta'])['estadoEncuesta' in user]     ## Ternario (ValorSiFalso, ValorSiVerdadero)[Condición]
    
    def toJSON(self):
        return {
            'id_usuario'     : self.id_usuario,
            'nombre'         : self.nombre,
            'empresa'        : self.empresa,
            'clave'          : self.clave,
            'email'          : self.email,
            'cargo'          : self.cargo,
            'salario'        : self.salario,
            'jornada'        : self.jornada,
            'perfil'         : self.perfil,
            'centrocosto'    : self.centrocosto,
            'tipocontrato'   : self.tipocontrato,
            'estado'         : self.estado,
            'codigo'         : self.codigo,
            'estadoEncuesta' : self.estadoEncuesta}

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
            'centrocosto', 
            'tipocontrato', 
            'estado',
            'codigo',
            'estadoEncuesta')

usuario   = usuarioScheme()
usuarios  = usuarioScheme(many=True)