from odoo import models, fields, api


class MedicalHistory(models.Model):
    _name = 'cs.medical.history'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Historial Médico'
    _order = 'resident_id, entry_date desc'

    name = fields.Char(string='Referencia', compute='_compute_name', store=True)
    
    resident_id = fields.Many2one(
        'cs.resident',
        string='Residente',
        required=True,
        index=True,
        tracking=True
    )
    
    partner_id = fields.Many2one(
        'res.partner',
        string='Paciente (Contacto)',
        related='resident_id.partner_id',
        store=True,
        readonly=True
    )
    
    entry_date = fields.Date(
        string='Fecha del Registro',
        required=True,
        default=fields.Date.context_today,
        tracking=True
    )
    
    # TIPO DE REGISTRO
    entry_type = fields.Selection(
        [
            ('consulta', 'Consulta Médica'),
            ('diagnostico', 'Diagnóstico'),
            ('medicacion', 'Medicación'),
            ('procedimiento', 'Procedimiento'),
            ('resultados_lab', 'Resultados Laboratorio'),
            ('nota_enfermeria', 'Nota de Enfermería'),
            ('otro', 'Otro'),
        ],
        string='Tipo de Registro',
        required=True,
        tracking=True
    )
    
    # INFORMACIÓN MÉDICA
    title = fields.Char(string='Título', required=True)
    description = fields.Text(string='Descripción')
    
    # PROFESIONAL RESPONSABLE
    professional_id = fields.Many2one(
        'cs.worker',
        string='Profesional Responsable',
        tracking=True
    )
    
    # REFERENCIAS A OTROS REGISTROS
    consultation_id = fields.Many2one(
        'cs.medical.consultation',
        string='Consulta Médica Relacionada'
    )
    
    prescription_id = fields.Many2one(
        'cs.prescription',
        string='Prescripción Relacionada'
    )
    
    # DOCUMENTACIÓN
    attachment_ids = fields.Many2many(
        'ir.attachment',
        string='Archivos Adjuntos',
        help='Documentos, imágenes, resultados de laboratorio, etc.'
    )
    
    # INFORMACIÓN CLÍNICA ESPECÍFICA
    temperature = fields.Float(string='Temperatura (°C)')
    blood_pressure = fields.Char(string='Presión Arterial (mmHg)')
    heart_rate = fields.Float(string='Frecuencia Cardíaca (bpm)')
    respiratory_rate = fields.Float(string='Frecuencia Respiratoria (rpm)')
    oxygen_saturation = fields.Float(string='Saturación O2 (%)')
    weight = fields.Float(string='Peso (kg)')
    height = fields.Float(string='Altura (cm)')
    
    # NOTAS MÉDICAS
    clinical_notes = fields.Text(string='Notas Clínicas')
    treatment_plan = fields.Text(string='Plan de Tratamiento')
    follow_up_notes = fields.Text(string='Notas de Seguimiento')
    
    # CONFIDENCIALIDAD
    is_confidential = fields.Boolean(
        string='Información Confidencial',
        default=False,
        tracking=True
    )
    
    @api.depends('resident_id', 'entry_date', 'entry_type')
    def _compute_name(self):
        """Genera nombre automático"""
        type_dict = dict(self._fields['entry_type'].selection)
        for record in self:
            if record.resident_id and record.entry_date:
                resident_name = record.resident_id.name
                entry_type = type_dict.get(record.entry_type, 'Registro')
                date_str = record.entry_date.strftime('%d/%m/%Y')
                record.name = f"{entry_type} - {resident_name} ({date_str})"
            else:
                record.name = "Historial Médico"

    def action_mark_confidential(self):
        """Marcar como información confidencial"""
        self.is_confidential = True

    def action_unmark_confidential(self):
        """Desmarcar como información confidencial"""
        self.is_confidential = False
