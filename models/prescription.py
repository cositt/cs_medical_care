from odoo import models, fields, api


class Prescription(models.Model):
    _name = 'cs.prescription'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Prescripción Médica'
    _order = 'prescription_date desc'

    name = fields.Char(string='Referencia', compute='_compute_name', store=True)
    
    # INFORMACIÓN DE LA PRESCRIPCIÓN
    resident_id = fields.Many2one(
        'cs.resident',
        string='Residente',
        required=True,
        tracking=True
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Paciente (Contacto)',
        related='resident_id.partner_id',
        store=True,
        readonly=True
    )
    
    consultation_id = fields.Many2one(
        'cs.medical.consultation',
        string='Consulta Médica',
        tracking=True,
        help='Consulta que origina la prescripción'
    )
    
    medical_professional_id = fields.Many2one(
        'cs.worker',
        string='Médico Prescriptor',
        required=True,
        tracking=True,
        domain=[('job_title', '=', 'médico')]
    )
    
    prescription_date = fields.Date(
        string='Fecha Prescripción',
        required=True,
        default=fields.Date.context_today,
        tracking=True
    )
    
    # DETALLES DE MEDICAMENTOS
    prescription_line_ids = fields.One2many(
        'cs.prescription.line',
        'prescription_id',
        string='Medicamentos'
    )
    
    # INSTRUCCIONES
    instructions = fields.Text(
        string='Instrucciones Especiales',
        help='Instrucciones adicionales para el paciente'
    )
    
    # ESTADO
    state = fields.Selection(
        [
            ('draft', 'Borrador'),
            ('activa', 'Activa'),
            ('pausada', 'Pausada'),
            ('finalizada', 'Finalizada'),
            ('cancelada', 'Cancelada'),
        ],
        string='Estado',
        default='draft',
        tracking=True
    )
    
    @api.depends('resident_id', 'prescription_date', 'medical_professional_id')
    def _compute_name(self):
        """Genera nombre automático"""
        for record in self:
            if record.resident_id and record.prescription_date:
                resident_name = record.resident_id.name
                date_str = record.prescription_date.strftime('%d/%m/%Y')
                record.name = f"Rx - {resident_name} ({date_str})"
            else:
                record.name = "Prescripción"

    def action_activate(self):
        """Activar prescripción"""
        self.state = 'activa'

    def action_pause(self):
        """Pausar prescripción"""
        self.state = 'pausada'

    def action_finish(self):
        """Finalizar prescripción"""
        self.state = 'finalizada'

    def action_cancel(self):
        """Cancelar prescripción"""
        self.state = 'cancelada'


class PrescriptionLine(models.Model):
    _name = 'cs.prescription.line'
    _description = 'Línea de Prescripción'
    _order = 'sequence'

    prescription_id = fields.Many2one(
        'cs.prescription',
        string='Prescripción',
        required=True,
        ondelete='cascade'
    )
    
    sequence = fields.Integer(default=10, string='Secuencia')
    
    medication_name = fields.Char(
        string='Nombre del Medicamento',
        required=True
    )
    
    dosage = fields.Char(
        string='Dosis',
        required=True,
        help='Ej: 500mg, 2 comprimidos'
    )
    
    frequency = fields.Selection(
        [
            ('cada_hora', 'Cada hora'),
            ('cada_2_horas', 'Cada 2 horas'),
            ('cada_4_horas', 'Cada 4 horas'),
            ('cada_6_horas', 'Cada 6 horas'),
            ('cada_8_horas', 'Cada 8 horas'),
            ('cada_12_horas', 'Cada 12 horas'),
            ('diariamente', 'Una vez al día'),
            ('dos_veces_dia', 'Dos veces al día'),
            ('tres_veces_dia', 'Tres veces al día'),
            ('cuatro_veces_dia', 'Cuatro veces al día'),
            ('segun_necesidad', 'Según sea necesario'),
        ],
        string='Frecuencia',
        required=True
    )
    
    duration_days = fields.Integer(
        string='Duración (días)',
        help='Número de días que debe tomar el medicamento'
    )
    
    via = fields.Selection(
        [
            ('oral', 'Oral'),
            ('intramuscular', 'Intramuscular'),
            ('intravenosa', 'Intravenosa'),
            ('subcutanea', 'Subcutánea'),
            ('topica', 'Tópica'),
            ('inhalada', 'Inhalada'),
        ],
        string='Vía de Administración',
        default='oral'
    )
    
    notes = fields.Text(string='Notas')
