from odoo import models, fields

class Profesor(models.Model):
    _name = 'gestion_academy.profesor'
    _description = 'Profesor'
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
        for profesor in self:
            profesor.nombre_completo = f"{profesor.nombre} {profesor.apellidos}"
    
    # Email
    email = fields.Char(string='Email', required=True)
    
    # Teléfono
    telefono = fields.Char(string='Teléfono')
    
    # Titulación/Especialización
    titulacion = fields.Text(string='Titulación o Especialización')
    
    # Años de experiencia
    experiencia_anios = fields.Integer(string='Años de Experiencia', default=0)
    
    # Relaciones
    # Many2many: Cursos que imparte (por la parte del profesor)
    cursos_ids = fields.Many2many(
        'gestion_academy.curso',
        'curso_profesor_rel',
        'profesor_id',
        'curso_id',
        string='Cursos Impartidos'
    )
    
    # One2many: Sesiones que enseña
    sesiones_ids = fields.One2many(
        'gestion_academy.sesion',
        'profesor_id',
        string='Sesiones'
    )
    
    # One2many: Clases que imparte
    clases_ids = fields.One2many(
        'gestion_academy.clase',
        'profesor_id',
        string='Clases'
    )
    
    # Estado
    estado = fields.Selection(
        selection=[
            ('activo', 'Activo'),
            ('inactivo', 'Inactivo'),
            ('excedencia', 'Excedencia'),
        ],
        string='Estado',
        default='activo'
    )
    
    # Curriculum (archivo)
    curriculum = fields.Binary(string='Curriculum', attachment=True)
    curriculum_filename = fields.Char(string='Nombre del Curriculum')
    
    # Fecha de contratación
    fecha_contratacion = fields.Date(string='Fecha de Contratación')
    
    # Bio/Descripción
    bio = fields.Text(string='Biografía')
    
    # Campos de auditoría
    fecha_creacion = fields.Datetime(string='Fecha de Creación', default=fields.Datetime.now)
    fecha_actualizacion = fields.Datetime(string='Fecha de Actualización', default=fields.Datetime.now)
