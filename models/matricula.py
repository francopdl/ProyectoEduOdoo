from odoo import models, fields, api


class Matricula(models.Model):
    _name = 'gestion_academy.matricula'
    _description = 'Matrícula de Alumno'
    _order = 'fecha_creacion desc'

    # Relaciones Many2one
    alumno_id = fields.Many2one(
        'gestion_academy.alumno',
        string='Alumno',
        required=True,
        ondelete='cascade'
    )
    
    sesion_id = fields.Many2one(
        'gestion_academy.sesion',
        string='Sesión',
        required=True,
        ondelete='cascade'
    )
    
    # Campo calculado: nombre de la matrícula
    nombre = fields.Char(
        string='Matrícula',
        compute='_compute_nombre',
        store=True
    )
    
    @api.depends('alumno_id', 'sesion_id')
    def _compute_nombre(self):
        for matricula in self:
            if matricula.alumno_id and matricula.sesion_id:
                matricula.nombre = f"{matricula.alumno_id.nombre_completo} - {matricula.sesion_id.nombre}"
            else:
                matricula.nombre = "Nueva Matrícula"
    
    # Estado de la matrícula
    estado = fields.Selection(
        selection=[
            ('borrador', 'Borrador'),
            ('confirmada', 'Confirmada'),
            ('pagada', 'Pagada'),
            ('cancelada', 'Cancelada'),
        ],
        string='Estado',
        default='borrador',
        required=True
    )
    
    # Precio de la matrícula
    precio = fields.Float(
        string='Precio',
        related='sesion_id.curso_id.precio',
        store=True
    )
    
    # Datos de pago
    fecha_pago = fields.Date(string='Fecha de Pago')
    metodo_pago = fields.Selection(
        selection=[
            ('efectivo', 'Efectivo'),
            ('tarjeta', 'Tarjeta'),
            ('transferencia', 'Transferencia'),
            ('cheque', 'Cheque'),
            ('otro', 'Otro'),
        ],
        string='Método de Pago'
    )
    
    # Referencia de pago
    referencia_pago = fields.Char(string='Referencia de Pago')
    
    # Campos de auditoría
    fecha_creacion = fields.Datetime(string='Fecha de Creación', default=fields.Datetime.now)
    fecha_actualizacion = fields.Datetime(string='Fecha de Actualización', default=fields.Datetime.now)
    
    # Métodos de transición de estado
    def action_confirmar(self):
        """Cambiar estado de borrador a confirmada"""
        self.estado = 'confirmada'
    
    def action_pagar(self):
        """Cambiar estado de confirmada a pagada"""
        if self.estado != 'confirmada':
            raise ValueError("La matrícula debe estar en estado Confirmada para pagar")
        self.estado = 'pagada'
        self.fecha_pago = fields.Date.today()
    
    def action_cancelar(self):
        """Cambiar estado a cancelada"""
        self.estado = 'cancelada'
    
    # Restricción: Una matrícula por alumno-sesión
    _sql_constraints = [
        ('unique_alumno_sesion', 'unique(alumno_id, sesion_id)', 
         'Ya existe una matrícula para este alumno en esta sesión')
    ]
