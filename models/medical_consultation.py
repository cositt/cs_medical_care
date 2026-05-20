from odoo import models, fields, api
from datetime import datetime


class MedicalConsultation(models.Model):
    _name = 'cs.medical.consultation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Consulta Médica'
    _order = 'consultation_date desc'

    name = fields.Char(string='Referencia', compute='_compute_name', store=True)
    
    # INFORMACIÓN DE LA CONSULTA
    resident_id = fields.Many2one(
        'cs.resident',
        string='Residente',
        required=True,
        tracking=True,
        help='Residente que asiste a la consulta'
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Paciente (Contacto)',
        related='resident_id.partner_id',
        store=True,
        readonly=True
    )
    
    medical_professional_id = fields.Many2one(
        'cs.worker',
        string='Profesional Médico',
        required=True,
        tracking=True,
        domain=[('job_title', 'in', ['médico', 'enfermero'])],
        help='Médico o profesional que realiza la consulta'
    )
    
    consultation_date = fields.Datetime(
        string='Fecha y Hora de Consulta',
        required=True,
        default=fields.Datetime.now,
        tracking=True
    )
    
    consultation_type = fields.Selection(
        [
            ('general', 'General'),
            ('seguimiento', 'Seguimiento'),
            ('urgencia', 'Urgencia'),
            ('especializada', 'Especializada'),
        ],
        string='Tipo de Consulta',
        default='general',
        tracking=True
    )
    
    # MOTIVO Y DIAGNÓSTICO
    chief_complaint = fields.Text(
        string='Motivo de Consulta',
        help='Síntomas o razón principal de la consulta'
    )
    diagnosis = fields.Text(string='Diagnóstico')
    diagnosis_cie10_code = fields.Char(string='Código CIE-10', size=10)
    diagnosis_cie10_name = fields.Char(string='Diagnóstico CIE-10')
    notes = fields.Text(string='Observaciones Clínicas')
    
    # TEMPLATE PARA EVALUACIÓN
    assessment_template_id = fields.Many2one(
        'cs.followup.template',
        string='Plantilla de Evaluación',
        domain=[('state', '=', 'published')],
        help='Formulario de evaluación a usar en la consulta'
    )
    
    assessment_id = fields.Many2one(
        'cs.followup.assessment',
        string='Evaluación Realizada',
        help='Registro de evaluación completada en la consulta'
    )
    
    # ESTADO
    state = fields.Selection(
        [
            ('programada', 'Programada'),
            ('en_curso', 'En Curso'),
            ('completada', 'Completada'),
            ('cancelada', 'Cancelada'),
        ],
        string='Estado',
        default='programada',
        tracking=True
    )
    
    _order = 'consultation_date desc'

    @api.depends('resident_id', 'consultation_date', 'medical_professional_id')
    def _compute_name(self):
        """Genera nombre automático de la consulta"""
        for record in self:
            if record.resident_id and record.consultation_date:
                resident_name = record.resident_id.name
                date_str = record.consultation_date.strftime('%d/%m/%Y %H:%M')
                record.name = f"Consulta - {resident_name} ({date_str})"
            else:
                record.name = "Consulta Médica"

    @api.onchange('assessment_template_id')
    def _onchange_assessment_template_id(self):
        """Crear evaluación cuando se selecciona un template"""
        if self.assessment_template_id:
            if not self.assessment_id:
                assessment = self.env['cs.followup.assessment'].create({
                    'template_id': self.assessment_template_id.id,
                    'patient_id': self.partner_id.id,
                    'clinician_id': self.env.user.id,
                    'assessment_date': self.consultation_date.date() if self.consultation_date else fields.Date.context_today(self),
                })
                self.assessment_id = assessment.id

    def action_mark_in_progress(self):
        """Marcar consulta como en curso"""
        self.state = 'en_curso'

    def action_mark_completed(self):
        """Marcar consulta como completada"""
        if self.assessment_id and self.assessment_id.state != 'done':
            self.assessment_id.action_mark_done()
        self.state = 'completada'

    def action_cancel(self):
        """Cancelar consulta"""
        self.state = 'cancelada'

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        admission_id = self.env.context.get('default_admission_id')
        if admission_id and records:
            self.env['cs.admission.process'].browse(admission_id).medical_consultation_id = records[0]
        return records
