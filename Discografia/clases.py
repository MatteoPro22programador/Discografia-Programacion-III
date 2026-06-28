class Compania:
    def __init__(self):
        self.id_compania = ""
        self.nombre      = ""
        self.direccion   = ""

class Grabacion:
    def __init__(self):
        self.titulo      = ""
        self.categoria   = ""
        self.num_temas   = ""
        self.descripcion = ""
        self.id_compania = ""

class Formato:
    def __init__(self):
        self.id_formato  = ""
        self.tipo        = ""
        self.conservacion = ""
        self.titulo      = ""

class Interprete:
    def __init__(self):
        self.id_interprete = ""
        self.nombre        = ""
        self.descripcion   = ""

class Participa:
    def __init__(self):
        self.id_interprete = ""
        self.titulo        = ""
        self.fecha         = ""