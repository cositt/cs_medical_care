from odoo import _, api, fields, models


class ResidentMedical(models.Model):
    _inherit = "cs.resident"

    weight_kg = fields.Float(string="Peso (kg)")
    height_cm = fields.Float(string="Talla (cm)")

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
    medical_prn_rescue_ids = fields.One2many(
        "cs.medical.prn.rescue",
        "resident_id",
        string="PRN / Rescates enfermería",
    )

    # Enfermería
    allergies = fields.Text(string="Alergias conocidas")
    current_medications = fields.Text(string="Medicación actual")
    nursing_notes = fields.Text(string="Notas de enfermería")
    test_alcohol = fields.Boolean(string="Test alcohol realizado")
    test_alcohol_result = fields.Char(string="Resultado alcohol")
    test_drugs = fields.Boolean(string="Test multidrogas realizado")
    test_drugs_result = fields.Char(string="Resultado multidrogas")

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

    def action_print_emergency_sheet(self):
        self.ensure_one()
        return self.env.ref("cs_medical_care.action_report_emergency_sheet").report_action(self)

    def get_emergency_sheet_data(self):
        self.ensure_one()

        freq_labels = dict(self.env["cs.prescription.line"]._fields["frequency"].selection)
        via_labels = dict(self.env["cs.prescription.line"]._fields["via"].selection)
        rescue_type_labels = dict(self.env["cs.medical.rescue"]._fields["scenario_type"].selection)
        rescue_outcome_labels = dict(self.env["cs.medical.rescue"]._fields["outcome"].selection)
        prn_route_labels = dict(self.env["cs.medical.prn.rescue"]._fields["route"].selection)
        treatment_type_labels = dict(self.env["cs.medical.treatment"]._fields["treatment_type"].selection)

        # Alergias: admission process (primario) → piai assessment (fallback)
        allergies = ""
        AdmissionModel = self.env.get("cs.admission.process")
        if AdmissionModel:
            admission = AdmissionModel.sudo().search([("resident_id", "=", self.id)], limit=1)
            if admission:
                allergies = admission.allergies or ""
        if not allergies:
            PiaiModel = self.env.get("cs.piai")
            if PiaiModel:
                piai = PiaiModel.sudo().search([("resident_id", "=", self.id)], limit=1)
                if piai:
                    PiaiAssessmentModel = self.env.get("cs.piai.assessment")
                    if PiaiAssessmentModel:
                        pa = PiaiAssessmentModel.sudo().search([("piai_id", "=", piai.id)], limit=1)
                        if pa:
                            allergies = getattr(pa, "allergies_text", "") or ""

        # Prescripciones activas con sus líneas
        prescriptions = []
        for rx in self.prescription_ids.filtered(lambda p: p.state == "activa"):
            for line in rx.prescription_line_ids:
                prescriptions.append({
                    "medication": line.medication_name,
                    "dosage": line.dosage,
                    "frequency": freq_labels.get(line.frequency, line.frequency or ""),
                    "via": via_labels.get(line.via, line.via or ""),
                    "notes": line.notes or "",
                    "doctor": rx.medical_professional_id.name or "",
                    "date": rx.prescription_date,
                })

        # Tratamientos activos
        treatments = []
        for t in self.medical_treatment_ids.filtered(lambda t: t.state in ["active", "planned"]):
            treatments.append({
                "title": t.title,
                "type": treatment_type_labels.get(t.treatment_type, t.treatment_type),
                "start": t.start_date,
                "responsible": t.responsible_id.name or "",
                "description": t.description or "",
            })

        # Últimos 5 rescates asistenciales
        rescues = []
        for r in self.medical_rescue_ids[:5]:
            rescues.append({
                "datetime": r.intervention_datetime,
                "type": rescue_type_labels.get(r.scenario_type, r.scenario_type),
                "findings": r.findings or "",
                "actions": r.actions_performed or "",
                "outcome": rescue_outcome_labels.get(r.outcome, r.outcome or ""),
            })

        # Últimos 5 PRN farmacológicos
        prn_list = []
        for p in self.env["cs.medical.prn.rescue"].search([("resident_id", "=", self.id)], limit=5):
            prn_list.append({
                "datetime": p.rescue_datetime,
                "medication": p.medication_name,
                "dose": p.dose,
                "route": prn_route_labels.get(p.route, p.route),
                "reason": p.reason or "",
                "professional": p.professional_id.name or "",
                "effect": p.effect_observed or "",
            })

        # Diagnósticos médicos (últimas 5 consultas completadas con diagnóstico)
        diagnoses = []
        for c in self.consultation_ids.filtered(lambda c: c.diagnosis and c.state == "completada")[:5]:
            diagnoses.append({
                "date": c.consultation_date,
                "diagnosis": c.diagnosis,
                "cie10_code": c.diagnosis_cie10_code or "",
                "cie10_name": c.diagnosis_cie10_name or "",
            })

        # Evaluación psicológica más reciente
        psych_data = None
        AssessmentModel = self.env.get("cs.initial.assessment")
        if AssessmentModel:
            pa = AssessmentModel.sudo().search(
                [("resident_id", "=", self.id)], order="assessment_date desc", limit=1
            )
            if pa:
                psych_data = {
                    "date": pa.assessment_date,
                    "psychologist": pa.psychologist_id.name or "",
                    "hypothesis": pa.initial_hypothesis or "",
                    "risk": pa.risk_notes or "",
                    "background": pa.background_summary or "",
                    "recommendations": pa.recommendations or "",
                }

        # Historial clínico: últimas 10 entradas
        history_type_labels = dict(self.env["cs.medical.history"]._fields["entry_type"].selection)
        history = []
        for h in self.medical_history_ids[:10]:
            history.append({
                "date": h.entry_date,
                "type": history_type_labels.get(h.entry_type, h.entry_type),
                "title": h.title,
                "description": h.description or "",
                "clinical_notes": h.clinical_notes or "",
                "treatment_plan": h.treatment_plan or "",
                "professional": h.professional_id.name or "",
            })

        return {
            "allergies": allergies,
            "prescriptions": prescriptions,
            "treatments": treatments,
            "rescues": rescues,
            "prn_list": prn_list,
            "diagnoses": diagnoses,
            "psych_data": psych_data,
            "history": history,
            "generated_at": fields.Datetime.now(),
        }
