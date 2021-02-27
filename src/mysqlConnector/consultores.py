from src import db, ma

class Consultores(db.Model):
    id        = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement = True)
    empresa   = db.Column(db.Integer, nullable = False)
    consultor = db.Column(db.Integer, nullable = False)
    estado    = db.Column(db.String(3), nullable = False)
    
    def __init__(self, id, empresa, consultor, estado):
        self.id        = id
        self.empresa   = empresa
        self.consultor = consultor
        self.estado    = estado
    
    def __init__(self, cons):
        self.id        = cons['id']
        self.empresa   = cons['empresa']
        self.consultor = cons['consultor'] 
        self.estado    = cons['estado']
    
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