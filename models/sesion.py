from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Sesion(models.Model):
    _name = 'gestion_academy.sesion'
    _description = 'Sesión del Curso'
    _order = 'fecha_inicio desc'

    # Campos básicos
    nombre = fields.Char(
        string='Nombre de la Sesión',
        compute='_compute_nombre',
        store=True
    )
    
    def _compute_nombre(self):
        for sesion in self:
            if sesion.curso_id and sesion.fecha_inicio:
                try:
                    sesion.nombre = f"{sesion.curso_id.nombre} - {sesion.fecha_inicio.strftime('%Y-%m-%d')}"
                except:
                    sesion.nombre = "Nueva Sesión"
            else:
                sesion.nombre = "Nueva Sesión"
    
    # Relaciones Many2one
    # Cada sesión pertenece a un curso
    curso_id = fields.Many2one(
        'gestion_academy.curso',
        string='Curso',
        required=True,
        ondelete='cascade'
    )
    
    # Cada sesión tiene un profesor
    profesor_id = fields.Many2one(
        'gestion_academy.profesor',
        string='Profesor',
        required=True,
        ondelete='restrict'
    )
    
    # Fecha de inicio
    fecha_inicio = fields.Datetime(string='Fecha de Inicio', required=True)
    
    # Duración en minutos
    duracion_minutos = fields.Integer(string='Duración (minutos)', required=True, default=90)
    
    # Fecha de fin (calculada)
    fecha_fin = fields.Datetime(
        string='Fecha de Fin',
        compute='_compute_fecha_fin',
        store=True
    )
    
    def _compute_fecha_fin(self):
        from datetime import timedelta
        for sesion in self:
            if sesion.fecha_inicio and sesion.duracion_minutos:
                sesion.fecha_fin = sesion.fecha_inicio + timedelta(minutes=sesion.duracion_minutos)
            else:
                sesion.fecha_fin = None
    
    # Número de asientos disponibles
    asientos_totales = fields.Integer(string='Total de Asientos', required=True, default=20)
    
    # Asientos ocupados (calculado)
    asientos_ocupados = fields.Integer(
        string='Asientos Ocupados',
        compute='_compute_asientos_ocupados',
        store=True
    )
    
    def _compute_asientos_ocupados(self):
        for sesion in self:
            sesion.asientos_ocupados = len(sesion.alumnos_asistentes_ids)
    
    # Asientos disponibles (calculado)
    asientos_disponibles = fields.Integer(
        string='Asientos Disponibles',
        compute='_compute_asientos_disponibles',
        store=False
    )
    
    def _compute_asientos_disponibles(self):
        for sesion in self:
            sesion.asientos_disponibles = sesion.asientos_totales - sesion.asientos_ocupados
    
    # Porcentaje de ocupación
    porcentaje_ocupacion = fields.Float(
        string='% Ocupación',
        compute='_compute_porcentaje_ocupacion',
        store=True
    )
    
    @api.depends('asientos_ocupados', 'asientos_totales')
    def _compute_porcentaje_ocupacion(self):
        for sesion in self:
            if sesion.asientos_totales > 0:
                sesion.porcentaje_ocupacion = (sesion.asientos_ocupados / sesion.asientos_totales) * 100
            else:
                sesion.porcentaje_ocupacion = 0.0
    
    # Color de ocupación para ProgressBar
    color_ocupacion = fields.Selection(
        selection=[
            ('green', 'Verde - Bajo ocupación'),
            ('yellow', 'Amarillo - Ocupación media'),
            ('orange', 'Naranja - Ocupación alta'),
            ('red', 'Rojo - Sesión llena'),
        ],
        string='Color Ocupación',
        compute='_compute_color_ocupacion',
        store=True
    )
    
    @api.depends('porcentaje_ocupacion')
    def _compute_color_ocupacion(self):
        for sesion in self:
            if sesion.porcentaje_ocupacion >= 100:
                sesion.color_ocupacion = 'red'
            elif sesion.porcentaje_ocupacion >= 80:
                sesion.color_ocupacion = 'orange'
            elif sesion.porcentaje_ocupacion >= 50:
                sesion.color_ocupacion = 'yellow'
            else:
                sesion.color_ocupacion = 'green'
    
    # Many2many: Alumnos asistentes
    alumnos_asistentes_ids = fields.Many2many(
        'gestion_academy.alumno',
        'sesion_alumno_rel',
        'sesion_id',
        'alumno_id',
        string='Alumnos Asistentes'
    )
    
    # Ubicación/Aula
    ubicacion = fields.Char(string='Ubicación/Aula')
    
    # Descripción de la sesión
    descripcion = fields.Text(string='Descripción')
    
    # Estado
    estado = fields.Selection(
        selection=[
            ('programada', 'Programada'),
            ('en_curso', 'En Curso'),
            ('completada', 'Completada'),
            ('cancelada', 'Cancelada'),
            ('pospuesta', 'Pospuesta'),
        ],
        string='Estado',
        default='programada'
    )
    
    material_recursos = fields.Text(string='Material y Recursos')
    

    notas = fields.Text(string='Notas')
    

    fecha_creacion = fields.Datetime(string='Fecha de Creación', default=fields.Datetime.now)
    fecha_actualizacion = fields.Datetime(string='Fecha de Actualización', default=fields.Datetime.now)


    
    @api.constrains('asientos_ocupados', 'asientos_totales')
    def _check_asientos_disponibles(self):
        """Validar que no haya más alumnos inscritos que asientos disponibles"""
        for sesion in self:
            if sesion.asientos_ocupados > sesion.asientos_totales:
                raise ValidationError(
                    f"La sesión '{sesion.nombre}' no puede tener más alumnos inscritos ({sesion.asientos_ocupados}) "
                    f"que asientos totales ({sesion.asientos_totales})"
                )
    
    @api.constrains('profesor_id', 'fecha_inicio', 'fecha_fin')
    def _check_profesor_no_sesiones_simultaneas(self):
        """Validar que el profesor no tenga dos sesiones a la misma hora"""
        for sesion in self:
            if not sesion.profesor_id or not sesion.fecha_inicio or not sesion.fecha_fin:
                continue
            
            # Buscar otras sesiones del mismo profesor en horario conflictivo
            conflictivas = self.search([
                ('profesor_id', '=', sesion.profesor_id.id),
                ('id', '!=', sesion.id),
                ('fecha_inicio', '<', sesion.fecha_fin),
                ('fecha_fin', '>', sesion.fecha_inicio),
            ])
            
            if conflictivas:
                sesiones_conflictivas = ', '.join([s.nombre for s in conflictivas])
                raise ValidationError(
                    f"El profesor '{sesion.profesor_id.nombre_completo}' ya tiene asignada otra sesión "
                    f"en este horario: {sesiones_conflictivas}"
                )
