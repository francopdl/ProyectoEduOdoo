from odoo import models, fields

class Clase(models.Model):
    _name = 'gestion_academy.clase'
    _description = 'Clase/Grupo'
    _order = 'nombre'

    # Campos básicos
    nombre = fields.Char(string='Nombre de la Clase', required=True, index=True)
    
    # Código o identificador único
    codigo = fields.Char(string='Código', unique=True, required=True)
    
    # Descripción
    descripcion = fields.Text(string='Descripción')
    
    # Relaciones Many2one
    # Cada clase pertenece a un curso
    curso_id = fields.Many2one(
        'gestion_academy.curso',
        string='Curso',
        required=True,
        ondelete='cascade'
    )
    
    # Cada clase tiene un profesor
    profesor_id = fields.Many2one(
        'gestion_academy.profesor',
        string='Profesor Responsable',
        required=True,
        ondelete='restrict'
    )
    
    # Horario
    # Día de la semana
    dia_semana = fields.Selection(
        selection=[
            ('lunes', 'Lunes'),
            ('martes', 'Martes'),
            ('miercoles', 'Miércoles'),
            ('jueves', 'Jueves'),
            ('viernes', 'Viernes'),
            ('sabado', 'Sábado'),
            ('domingo', 'Domingo'),
        ],
        string='Día de la Semana',
        required=True
    )
    
    # Hora de inicio
    hora_inicio = fields.Float(string='Hora de Inicio', required=True, help='Ej: 9.5 para 9:30')
    
    # Hora de fin
    hora_fin = fields.Float(string='Hora de Fin', required=True, help='Ej: 11.0 para 11:00')
    
    # Duración calculada
    duracion_horas = fields.Float(
        string='Duración (horas)',
        compute='_compute_duracion_horas',
        store=True
    )
    
    def _compute_duracion_horas(self):
        for clase in self:
            clase.duracion_horas = clase.hora_fin - clase.hora_inicio
    
    # Ubicación/Aula
    ubicacion = fields.Char(string='Ubicación/Aula', required=True)
    
    # Capacidad máxima
    capacidad_maxima = fields.Integer(string='Capacidad Máxima', required=True, default=25)
    
    # Many2many: Alumnos inscritos en la clase
    alumnos_ids = fields.Many2many(
        'gestion_academy.alumno',
        'clase_alumno_rel',
        'clase_id',
        'alumno_id',
        string='Alumnos Inscritos'
    )
    
    # Cantidad de alumnos (calculada)
    cantidad_alumnos = fields.Integer(
        string='Cantidad de Alumnos',
        compute='_compute_cantidad_alumnos',
        store=True
    )
    
    def _compute_cantidad_alumnos(self):
        for clase in self:
            clase.cantidad_alumnos = len(clase.alumnos_ids)
    
    # Lugares disponibles (calculado)
    lugares_disponibles = fields.Integer(
        string='Lugares Disponibles',
        compute='_compute_lugares_disponibles',
        store=False
    )
    
    def _compute_lugares_disponibles(self):
        for clase in self:
            clase.lugares_disponibles = clase.capacidad_maxima - clase.cantidad_alumnos
    
    # Estado
    estado = fields.Selection(
        selection=[
            ('planificada', 'Planificada'),
            ('activa', 'Activa'),
            ('finalizada', 'Finalizada'),
            ('cancelada', 'Cancelada'),
        ],
        string='Estado',
        default='planificada'
    )
    
    # Fecha de inicio del grupo
    fecha_inicio = fields.Date(string='Fecha de Inicio')
    
    # Fecha de fin del grupo
    fecha_fin = fields.Date(string='Fecha de Fin')
    
    # Nivel del grupo
    nivel = fields.Selection(
        selection=[
            ('A1', 'A1 - Beginner'),
            ('A2', 'A2 - Elementary'),
            ('B1', 'B1 - Intermediate'),
            ('B2', 'B2 - Upper Intermediate'),
            ('C1', 'C1 - Advanced'),
            ('C2', 'C2 - Proficiency'),
        ],
        string='Nivel',
        related='curso_id.nivel'
    )
    
    # Notas/Observaciones
    notas = fields.Text(string='Notas')
    
    # Campos de auditoría
    fecha_creacion = fields.Datetime(string='Fecha de Creación', default=fields.Datetime.now)
    fecha_actualizacion = fields.Datetime(string='Fecha de Actualización', default=fields.Datetime.now)
