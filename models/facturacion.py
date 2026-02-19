from odoo import models, fields

class Facturacion(models.Model):
    _name = 'gestion_academy.facturacion'
    _description = 'Facturación'
    _order = 'fecha_factura desc'

    # Campos básicos
    numero_factura = fields.Char(
        string='Número de Factura',
        required=True,
        unique=True,
        readonly=True,
        default='/'
    )
    
    # Relaciones Many2one
    # Cada factura esta asociada a un alumno
    alumno_id = fields.Many2one(
        'gestion_academy.alumno',
        string='Alumno',
        required=True,
        ondelete='restrict'
    )
    
    # Cada factura esta asociada a un curso
    curso_id = fields.Many2one(
        'gestion_academy.curso',
        string='Curso',
        required=True,
        ondelete='restrict'
    )
    
    # Fecha de factura
    fecha_factura = fields.Date(string='Fecha de Factura', required=True, default=fields.Date.today)
    
    # Cantidad/Monto
    cantidad = fields.Float(string='Cantidad/Monto', required=True, digits=(10, 2))
    
    # Concepto
    concepto = fields.Selection(
        selection=[
            ('matricula', 'Matrícula'),
            ('cuota_mensual', 'Cuota Mensual'),
            ('cuota_trimestral', 'Cuota Trimestral'),
            ('material_didactico', 'Material Didáctico'),
            ('examen', 'Examen'),
            ('certificado', 'Certificado'),
            ('otro', 'Otro'),
        ],
        string='Concepto',
        required=True
    )
    
    # Descripción del concepto
    descripcion = fields.Text(string='Descripción')
    
    # Fecha de pago
    fecha_pago = fields.Date(string='Fecha de Pago')
    
    # Estado de pago
    estado_pago = fields.Selection(
        selection=[
            ('pendiente', 'Pendiente'),
            ('parcial', 'Parcial'),
            ('pagado', 'Pagado'),
            ('vencido', 'Vencido'),
            ('anulado', 'Anulado'),
        ],
        string='Estado de Pago',
        default='pendiente'
    )
    
    # Monto pagado
    monto_pagado = fields.Float(
        string='Monto Pagado',
        digits=(10, 2),
        default=0.0
    )
    
    # Saldo pendiente (calculado)
    saldo_pendiente = fields.Float(
        string='Saldo Pendiente',
        compute='_compute_saldo_pendiente',
        store=True
    )
    
    def _compute_saldo_pendiente(self):
        for factura in self:
            factura.saldo_pendiente = factura.cantidad - factura.monto_pagado
    
    # Fecha de vencimiento
    fecha_vencimiento = fields.Date(string='Fecha de Vencimiento')
    
    # Método de pago
    metodo_pago = fields.Selection(
        selection=[
            ('efectivo', 'Efectivo'),
            ('transferencia', 'Transferencia Bancaria'),
            ('tarjeta_credito', 'Tarjeta de Crédito'),
            ('tarjeta_debito', 'Tarjeta de Débito'),
            ('cheque', 'Cheque'),
            ('otro', 'Otro'),
        ],
        string='Método de Pago'
    )
    
    # Número de referencia/Transacción
    referencia_transaccion = fields.Char(string='Referencia de Transacción')
    
    # Notas/Observaciones
    notas = fields.Text(string='Notas')
    
    # Impuestos
    impuesto_porcentaje = fields.Float(string='% Impuesto', default=0.0)
    impuesto_monto = fields.Float(
        string='Monto Impuesto',
        compute='_compute_impuesto_monto',
        store=True
    )
    
    def _compute_impuesto_monto(self):
        for factura in self:
            factura.impuesto_monto = (factura.cantidad * factura.impuesto_porcentaje) / 100
    
    # Total con impuestos
    total_con_impuestos = fields.Float(
        string='Total con Impuestos',
        compute='_compute_total_con_impuestos',
        store=True
    )
    
    def _compute_total_con_impuestos(self):
        for factura in self:
            factura.total_con_impuestos = factura.cantidad + factura.impuesto_monto
    
    # Recibo/Comprobante
    comprobante = fields.Binary(string='Comprobante', attachment=True)
    comprobante_filename = fields.Char(string='Nombre del Comprobante')
    
    # Campos de auditoría
    fecha_creacion = fields.Datetime(string='Fecha de Creación', default=fields.Datetime.now)
    fecha_actualizacion = fields.Datetime(string='Fecha de Actualización', default=fields.Datetime.now)
    usuario_creacion = fields.Many2one('res.users', string='Usuario que Creó', readonly=True, default=lambda self: self.env.user)
