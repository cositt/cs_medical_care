# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class MedicalPrnRescue(models.Model):
    _name = 'cs.medical.prn.rescue'
    _description = 'Rescate PRN farmacológico'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'rescue_datetime desc, id desc'

    name = fields.Char(string='Referencia', required=True, copy=False, default='/')
    resident_id = fields.Many2one(
        'cs.resident',
        string='Residente',
        required=True,
        index=True,
        tracking=True,
        ondelete='restrict',
    )
    rescue_datetime = fields.Datetime(
        string='Fecha y hora',
        required=True,
        default=fields.Datetime.now,
        tracking=True,
    )
    medication_name = fields.Char(
        string='Medicamento',
        required=True,
        tracking=True,
        help='Nombre del medicamento. Si cs_cima está instalado, se puede vincular al catálogo.',
    )
    dose = fields.Char(string='Dosis', required=True, tracking=True)
    route = fields.Selection(
        [
            ('oral', 'Oral'),
            ('sublingual', 'Sublingual'),
            ('intramuscular', 'Intramuscular'),
            ('intravenosa', 'Intravenosa'),
            ('subcutanea', 'Subcutánea'),
            ('topica', 'Tópica'),
            ('inhalada', 'Inhalada'),
            ('otro', 'Otro'),
        ],
        string='Vía de administración',
        required=True,
        default='oral',
        tracking=True,
    )
    reason = fields.Text(string='Motivo PRN', required=True, tracking=True)
    professional_id = fields.Many2one(
        'cs.worker',
        string='Administrado por',
        tracking=True,
        ondelete='set null',
        help='Monitora o profesional que administró el medicamento.',
    )
    effect_observed = fields.Text(string='Efecto observado')
    state = fields.Selection(
        [('draft', 'Borrador'), ('done', 'Registrado')],
        string='Estado',
        default='draft',
        tracking=True,
    )
    company_id = fields.Many2one(
        'res.company',
        string='Compañía',
        required=True,
        default=lambda self: self.env.company,
        index=True,
    )

    @api.model_create_multi
    def create(self, vals_list):
        seq = self.env['ir.sequence'].sudo()
        for vals in vals_list:
            if vals.get('name', '/') in ('/', False, None):
                vals['name'] = seq.next_by_code('cs.medical.prn.rescue') or '/'
        return super().create(vals_list)

    def action_confirm(self):
        for rec in self:
            rec.state = 'done'
