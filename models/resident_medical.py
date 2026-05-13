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
    medical_rescue_ids = fields.One2many(
        "cs.medical.rescue",
        "resident_id",
        string="Rescates",
    )
    medical_analgesia_ids = fields.One2many(
        "cs.medical.analgesia",
        "resident_id",
        string="Analgesia",
    )
    medical_clinic_test_ids = fields.One2many(
        "cs.medical.clinic.test",
        "resident_id",
        string="Tests clínicos",
    )
    medical_treatment_ids = fields.One2many(
        "cs.medical.treatment",
        "resident_id",
        string="Tratamientos",
    )
    medical_followup_ids = fields.One2many(
        "cs.medical.followup",
        "resident_id",
        string="Seguimiento",
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
    medical_rescue_count = fields.Integer(
        string="Nº rescates",
        compute="_compute_medical_counts",
    )
    medical_analgesia_count = fields.Integer(
        string="Nº analgesia",
        compute="_compute_medical_counts",
    )
    medical_test_count = fields.Integer(
        string="Nº tests",
        compute="_compute_medical_counts",
    )
    medical_treatment_count = fields.Integer(
        string="Nº tratamientos",
        compute="_compute_medical_counts",
    )
    medical_followup_pending_count = fields.Integer(
        string="Seguimientos pendientes",
        compute="_compute_medical_counts",
    )

    @api.depends(
        "prescription_ids",
        "prescription_ids.state",
        "consultation_ids",
        "medical_history_ids",
        "medical_rescue_ids",
        "medical_analgesia_ids",
        "medical_clinic_test_ids",
        "medical_treatment_ids",
        "medical_followup_ids",
        "medical_followup_ids.state",
    )
    def _compute_medical_counts(self):
        for rec in self:
            rec.prescription_active_count = len(
                rec.prescription_ids.filtered(lambda p: p.state == "activa")
            )
            rec.prescription_total_count = len(rec.prescription_ids)
            rec.consultation_count = len(rec.consultation_ids)
            rec.medical_history_count = len(rec.medical_history_ids)
            rec.medical_rescue_count = len(rec.medical_rescue_ids)
            rec.medical_analgesia_count = len(rec.medical_analgesia_ids)
            rec.medical_test_count = len(rec.medical_clinic_test_ids)
            rec.medical_treatment_count = len(rec.medical_treatment_ids)
            rec.medical_followup_pending_count = len(
                rec.medical_followup_ids.filtered(lambda f: f.state == "pending")
            )

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
            "name": _("Historia clínica (registros)"),
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

    def action_open_medical_rescues(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Rescates / intervenciones"),
            "res_model": "cs.medical.rescue",
            "view_mode": "list,form",
            "domain": [("resident_id", "=", self.id)],
            "context": {"default_resident_id": self.id},
        }

    def action_open_medical_analgesia(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Analgesia"),
            "res_model": "cs.medical.analgesia",
            "view_mode": "list,form",
            "domain": [("resident_id", "=", self.id)],
            "context": {"default_resident_id": self.id},
        }

    def action_open_medical_tests(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Tests / pruebas"),
            "res_model": "cs.medical.clinic.test",
            "view_mode": "list,form",
            "domain": [("resident_id", "=", self.id)],
            "context": {"default_resident_id": self.id},
        }

    def action_open_medical_treatments(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Tratamientos"),
            "res_model": "cs.medical.treatment",
            "view_mode": "list,form",
            "domain": [("resident_id", "=", self.id)],
            "context": {"default_resident_id": self.id},
        }

    def action_open_medical_followups(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Seguimiento"),
            "res_model": "cs.medical.followup",
            "view_mode": "list,form",
            "domain": [("resident_id", "=", self.id)],
            "context": {"default_resident_id": self.id},
        }
