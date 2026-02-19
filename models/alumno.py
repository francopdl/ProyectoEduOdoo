from odoo import models, fields

class Alumno(models.Model):
    _name = 'gestion_academy.alumno'
    _description = 'Alumno'
    _order = 'nombre'

    # Campos básicos
    nombre = fields.Char(string='Nombre', required=True, index=True)
    apellidos = fields.Char(string='Apellidos', required=True)
    
    # Campo calculado de nombre completo
    nombre_completo = fields.Char(
        string='Nombre Completo',
        compute='_compute_nombre_completo',
        store=True
    )
    
    def _compute_nombre_completo(self):
        for alumno in self:
            alumno.nombre_completo = f"{alumno.nombre} {alumno.apellidos}"
    
    # Email
    email = fields.Char(string='Email', required=True)
    
    # Teléfono
    telefono = fields.Char(string='Teléfono')
    
    # Fecha de nacimiento
    fecha_nacimiento = fields.Date(string='Fecha de Nacimiento')
    
    # Edad (calculada)
    edad = fields.Integer(
        string='Edad',
        compute='_compute_edad',
        store=False
    )
    
    def _compute_edad(self):
        from datetime import date
        for alumno in self:
            if alumno.fecha_nacimiento:
                hoje = date.today()
                alumno.edad = hoje.year - alumno.fecha_nacimiento.year - (
                    (hoje.month, hoje.day) < (alumno.fecha_nacimiento.month, alumno.fecha_nacimiento.day)
                )
            else:
                alumno.edad = 0
    
    # Nacionalidad
    nacionalidad = fields.Char(string='Nacionalidad')
    
    # Relaciones
    # Many2many: Cursos en los que está inscrito
    cursos_ids = fields.Many2many(
        'gestion_academy.curso',
        'curso_alumno_rel',
        'alumno_id',
        'curso_id',
        string='Cursos Inscritos'
    )
    
    # One2many: Facturas del alumno
    facturas_ids = fields.One2many(
        'gestion_academy.facturacion',
        'alumno_id',
        string='Facturas'
    )
    
    # Estado
    estado = fields.Selection(
        selection=[
            ('activo', 'Activo'),
            ('inactivo', 'Inactivo'),
            ('suspendido', 'Suspendido'),
            ('graduado', 'Graduado'),
        ],
        string='Estado',
        default='activo'
    )
    
    # Notas/Comentarios
    notas = fields.Text(string='Notas')
    
    # Saldo total facturado
    saldo_total = fields.Float(
        string='Saldo Total Facturado',
        compute='_compute_saldo_total',
        store=False
    )
    
    def _compute_saldo_total(self):
        for alumno in self:
            alumno.saldo_total = sum(factura.cantidad for factura in alumno.facturas_ids)
    
    # Documentos de identidad
    documento_identidad = fields.Char(string='Documento de Identidad')
    tipo_documento = fields.Selection(
        selection=[
            ('dni', 'DNI'),
            ('pasaporte', 'Pasaporte'),
            ('nie', 'NIE'),
        ],
        string='Tipo de Documento'
    )
    
    # Campos de auditoría
    fecha_creacion = fields.Datetime(string='Fecha de Creación', default=fields.Datetime.now)
    fecha_actualizacion = fields.Datetime(string='Fecha de Actualización', default=fields.Datetime.now)
