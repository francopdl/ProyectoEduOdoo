from odoo import models, fields

class Curso(models.Model):
    _name = 'gestion_academy.curso'
    _description = 'Curso'
    _order = 'nombre'

    # Campos básicos
    nombre = fields.Char(string='Título', required=True, index=True)
    descripcion = fields.Text(string='Descripción')
    
    # Nivel del curso (A1, A2, B1, B2, C1, C2)
    nivel = fields.Selection(
        selection=[
            ('A1', 'A1 - Beginner'),
            ('A2', 'A2 - Elementary'),
            ('B1', 'B1 - Intermediate'),
            ('B2', 'B2 - Upper Intermediate'),
            ('C1', 'C1 - Advanced'),
            ('C2', 'C2 - Proficiency'),
        ],
        string='Nivel CEFR',
        required=True
    )
    
    # Precio del curso
    precio = fields.Float(string='Precio', required=True, digits=(10, 2))
    
    # Relaciones
    # Many2one: Un curso tiene un profesor principal
    profesor_id = fields.Many2one(
        'gestion_academy.profesor',
        string='Profesor Principal',
        required=False,
        help='Profesor responsable principal del curso'
    )
    
    # Many2many: Un curso tiene múltiples profesores
    profesores_ids = fields.Many2many(
        'gestion_academy.profesor',
        'curso_profesor_rel',
        'curso_id',
        'profesor_id',
        string='Profesores Asignados'
    )
    
    # Many2many: Un curso tiene múltiples sesiones
    sesiones_ids = fields.One2many(
        'gestion_academy.sesion',
        'curso_id',
        string='Sesiones'
    )
    
    # Many2many: Un curso tiene múltiples clases
    clases_ids = fields.One2many(
        'gestion_academy.clase',
        'curso_id',
        string='Clases'
    )
    
    # Many2many: Alumnos inscritos en el curso
    alumnos_ids = fields.Many2many(
        'gestion_academy.alumno',
        'curso_alumno_rel',
        'curso_id',
        'alumno_id',
        string='Alumnos Inscritos'
    )
    
    # De solo lectura: Cantidad de alumnos
    cantidad_alumnos = fields.Integer(
        string='Cantidad de Alumnos',
        compute='_compute_cantidad_alumnos',
        store=True
    )
    
    def _compute_cantidad_alumnos(self):
        for curso in self:
            curso.cantidad_alumnos = len(curso.alumnos_ids)
    
    # Estado del curso
    estado = fields.Selection(
        selection=[
            ('draft', 'Borrador'),
            ('confirmado', 'Confirmado'),
            ('en_curso', 'En Curso'),
            ('finalizado', 'Finalizado'),
            ('cancelado', 'Cancelado'),
        ],
        string='Estado',
        default='draft'
    )
    
    # Campos de auditoría
    fecha_creacion = fields.Datetime(string='Fecha de Creación', default=fields.Datetime.now)
    fecha_actualizacion = fields.Datetime(string='Fecha de Actualización', default=fields.Datetime.now)
