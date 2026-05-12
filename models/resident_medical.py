from odoo import _, api, fields, models


class ResidentMedical(models.Model):
    _inherit = "cs.resident"

    prescription_ids = fields.One2many(
        "cs.prescription",
        "resident_id",
        string="Prescripciones",
    )
    consultation_ids = fields.One2many(
        "cs.medical.consultation",
        "resident_id",
        string="Consultas médicas",
    )
    medical_history_ids = fields.One2many(
        "cs.medical.history",
        "resident_id",
        string="Historial médico",
    )

    prescription_active_count = fields.Integer(
        string="Prescripciones activas",
        compute="_compute_medical_counts",
    )
    prescription_total_count = fields.Integer(
        string="Total prescripciones",
        compute="_compute_medical_counts",
    )
    consultation_count = fields.Integer(
        string="Nº consultas",
        compute="_compute_medical_counts",
    )
    medical_history_count = fields.Integer(
        string="Nº historial",
        compute="_compute_medical_counts",
    )

    @api.depends(
        "prescription_ids",
        "prescription_ids.state",
        "consultation_ids",
        "medical_history_ids",
    )
    def _compute_medical_counts(self):
        for rec in self:
            rec.prescription_active_count = len(
                rec.prescription_ids.filtered(lambda p: p.state == "activa")
            )
            rec.prescription_total_count = len(rec.prescription_ids)
            rec.consultation_count = len(rec.consultation_ids)
            rec.medical_history_count = len(rec.medical_history_ids)

    def action_open_medical_consultations(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Consultas médicas"),
            "res_model": "cs.medical.consultation",
            "view_mode": "list,form",
            "domain": [("resident_id", "=", self.id)],
            "context": {"default_resident_id": self.id},
        }

    def action_open_medical_history(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Historial médico"),
            "res_model": "cs.medical.history",
            "view_mode": "list,form",
            "domain": [("resident_id", "=", self.id)],
            "context": {"default_resident_id": self.id},
        }

    def action_open_prescriptions_all(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Prescripciones"),
            "res_model": "cs.prescription",
            "view_mode": "list,form",
            "domain": [("resident_id", "=", self.id)],
            "context": {"default_resident_id": self.id},
        }
