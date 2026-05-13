from odoo import api, fields, models
from odoo.exceptions import ValidationError


class MedicalRescue(models.Model):
    """Intervenciones / rescates asistenciales (caídas, crisis, etc.)."""

    _name = "cs.medical.rescue"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Rescate / intervención asistencial"
    _order = "intervention_datetime desc"

    name = fields.Char(string="Referencia", compute="_compute_name", store=True)
    resident_id = fields.Many2one(
        "cs.resident",
        string="Residente",
        required=True,
        index=True,
        tracking=True,
    )
    partner_id = fields.Many2one(
        "res.partner",
        string="Contacto",
        related="resident_id.partner_id",
        store=True,
        readonly=True,
    )
    intervention_datetime = fields.Datetime(
        string="Fecha y hora",
        required=True,
        default=fields.Datetime.now,
        tracking=True,
    )
    scenario_type = fields.Selection(
        [
            ("caida", "Caída"),
            ("convulsion", "Convulsión / crisis"),
            ("atragantamiento", "Atragantamiento"),
            ("alteracion_consciencia", "Alteración de consciencia"),
            ("dolor_toracico", "Dolor torácico"),
            ("hemorragia", "Hemorragia relevante"),
            ("agitacion", "Agitación / comportamiento de riesgo"),
            ("otro", "Otro"),
        ],
        string="Tipo de situación",
        required=True,
        tracking=True,
    )
    location_detail = fields.Char(
        string="Lugar (habitación, sala…)",
        help="Dónde ocurrió o se atendió la situación.",
    )
    findings = fields.Text(string="Hallazgos / circunstancias")
    actions_performed = fields.Text(
        string="Actuación realizada",
        help="Protocolo aplicado, primera ayuda, monitorización, etc.",
    )
    outcome = fields.Selection(
        [
            ("resuelto_centro", "Resuelto en centro"),
            ("observacion", "Observación / vigilancia"),
            ("traslado_hospital", "Traslado a hospital"),
            ("otro", "Otro desenlace"),
        ],
        string="Desenlace",
        tracking=True,
    )
    outcome_notes = fields.Text(string="Notas del desenlace")
    reporter_id = fields.Many2one(
        "cs.worker",
        string="Profesional que registra",
        tracking=True,
        domain=[
            (
                "job_title",
                "in",
                ["médico", "enfermero", "cuidador", "fisioterapeuta", "director"],
            )
        ],
    )
    consultation_id = fields.Many2one(
        "cs.medical.consultation",
        string="Consulta relacionada",
    )
    attachment_ids = fields.Many2many(
        "ir.attachment",
        string="Adjuntos",
        help="Informes, fotografías clínicas autorizadas, etc.",
    )

    @api.depends("resident_id", "intervention_datetime", "scenario_type")
    def _compute_name(self):
        scenario_labels = dict(self._fields["scenario_type"].selection)
        for rec in self:
            if rec.resident_id and rec.intervention_datetime:
                dt = fields.Datetime.context_timestamp(
                    rec, rec.intervention_datetime
                ).strftime("%d/%m/%Y %H:%M")
                lab = scenario_labels.get(rec.scenario_type, "Intervención")
                rec.name = f"Rescate ({lab}) — {rec.resident_id.name} ({dt})"
            else:
                rec.name = "Rescate"


class MedicalAnalgesia(models.Model):
    """Registro explícito de analgesia / control del dolor."""

    _name = "cs.medical.analgesia"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Registro de analgesia"
    _order = "administration_datetime desc"

    name = fields.Char(string="Referencia", compute="_compute_name", store=True)
    resident_id = fields.Many2one(
        "cs.resident",
        string="Residente",
        required=True,
        index=True,
        tracking=True,
    )
    partner_id = fields.Many2one(
        "res.partner",
        related="resident_id.partner_id",
        store=True,
        readonly=True,
    )
    administration_datetime = fields.Datetime(
        string="Fecha y hora administración",
        required=True,
        default=fields.Datetime.now,
        tracking=True,
    )
    pain_scale_before = fields.Integer(string="EVA / intensidad antes (0–10)")
    pain_scale_after = fields.Integer(string="EVA / intensidad después (0–10)")
    medication_description = fields.Char(
        string="Medicación / medida",
        required=True,
        help="Principio activo, medicamento o medida no farmacológica.",
    )
    dose = fields.Char(string="Dosis")
    route = fields.Selection(
        [
            ("oral", "Oral"),
            ("intramuscular", "Intramuscular"),
            ("intravenosa", "Intravenosa"),
            ("subcutanea", "Subcutánea"),
            ("topica", "Tópica"),
            ("inhalada", "Inhalada"),
            ("otra", "Otra"),
        ],
        string="Vía",
        default="oral",
    )
    professional_id = fields.Many2one(
        "cs.worker",
        string="Profesional",
        tracking=True,
        domain=[("job_title", "in", ["médico", "enfermero"])],
    )
    consultation_id = fields.Many2one(
        "cs.medical.consultation",
        string="Consulta relacionada",
    )
    prescription_id = fields.Many2one(
        "cs.prescription",
        string="Prescripción relacionada",
        help="Si procede de pauta médica registrada.",
    )
    notes = fields.Text(string="Observaciones")

    @api.constrains("pain_scale_before", "pain_scale_after")
    def _check_pain_scales(self):
        for rec in self:
            for fld in ("pain_scale_before", "pain_scale_after"):
                val = rec[fld]
                if val is not False and val is not None and (val < 0 or val > 10):
                    raise ValidationError(
                        "Las escalas de dolor deben estar entre 0 y 10."
                    )

    @api.depends("resident_id", "administration_datetime", "medication_description")
    def _compute_name(self):
        for rec in self:
            if rec.resident_id and rec.administration_datetime:
                dt = fields.Datetime.context_timestamp(
                    rec, rec.administration_datetime
                ).strftime("%d/%m/%Y %H:%M")
                med = rec.medication_description or "Analgesia"
                rec.name = f"Analgesia — {med} — {rec.resident_id.name} ({dt})"
            else:
                rec.name = "Analgesia"


class MedicalClinicTest(models.Model):
    """Pruebas complementarias (laboratorio, imagen, etc.)."""

    _name = "cs.medical.clinic.test"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Prueba / test clínico"
    _order = "test_date desc"

    name = fields.Char(string="Referencia", compute="_compute_name", store=True)
    resident_id = fields.Many2one(
        "cs.resident",
        string="Residente",
        required=True,
        index=True,
        tracking=True,
    )
    partner_id = fields.Many2one(
        "res.partner",
        related="resident_id.partner_id",
        store=True,
        readonly=True,
    )
    test_date = fields.Date(
        string="Fecha prueba / resultado",
        required=True,
        default=fields.Date.context_today,
        tracking=True,
    )
    test_category = fields.Selection(
        [
            ("lab", "Laboratorio"),
            ("imaging", "Imagen"),
            ("functional", "Funcional"),
            ("cognitive", "Cognitivo"),
            ("ecg", "ECG / cardiaca"),
            ("other", "Otra"),
        ],
        string="Tipo",
        required=True,
        tracking=True,
    )
    title = fields.Char(string="Nombre / estudio", required=True)
    result_summary = fields.Text(string="Resultado / conclusiones")
    ordered_by_id = fields.Many2one(
        "cs.worker",
        string="Solicitado por",
        domain=[("job_title", "in", ["médico", "enfermero"])],
    )
    consultation_id = fields.Many2one(
        "cs.medical.consultation",
        string="Consulta relacionada",
    )
    attachment_ids = fields.Many2many(
        "ir.attachment",
        string="Informes adjuntos",
    )

    @api.depends("resident_id", "test_date", "title", "test_category")
    def _compute_name(self):
        labels = dict(self._fields["test_category"].selection)
        for rec in self:
            if rec.resident_id and rec.test_date:
                cat = labels.get(rec.test_category, "Test")
                ttl = rec.title or "Estudio"
                ds = rec.test_date.strftime("%d/%m/%Y")
                rec.name = f"{cat} — {ttl} — {rec.resident_id.name} ({ds})"
            else:
                rec.name = "Test clínico"


class MedicalTreatment(models.Model):
    """Tratamientos no ligados línea a línea a la prescripción (curas, FNP, etc.)."""

    _name = "cs.medical.treatment"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Tratamiento"
    _order = "start_date desc"

    name = fields.Char(string="Denominación", compute="_compute_name", store=True)
    resident_id = fields.Many2one(
        "cs.resident",
        string="Residente",
        required=True,
        index=True,
        tracking=True,
    )
    partner_id = fields.Many2one(
        "res.partner",
        related="resident_id.partner_id",
        store=True,
        readonly=True,
    )
    title = fields.Char(string="Título tratamiento", required=True)
    treatment_type = fields.Selection(
        [
            ("farmacologico", "Farmacológico (pauta resumida)"),
            ("heridas", "Heridas / pie diabético"),
            ("fisioterapia", "Fisioterapia / rehabilitación"),
            ("respiratorio", "Respiratorio"),
            ("nutricional", "Nutrición"),
            ("otro", "Otro"),
        ],
        string="Tipo",
        required=True,
        tracking=True,
    )
    start_date = fields.Date(
        string="Inicio",
        required=True,
        default=fields.Date.context_today,
        tracking=True,
    )
    end_date = fields.Date(string="Fin previsto / alta tratamiento")
    description = fields.Text(string="Descripción / objetivos")
    state = fields.Selection(
        [
            ("planned", "Planificado"),
            ("active", "Activo"),
            ("completed", "Completado"),
            ("suspended", "Suspendido"),
        ],
        string="Estado",
        default="planned",
        tracking=True,
    )
    responsible_id = fields.Many2one(
        "cs.worker",
        string="Responsable",
        domain=[("job_title", "in", ["médico", "enfermero", "fisioterapeuta"])],
    )
    consultation_id = fields.Many2one(
        "cs.medical.consultation",
        string="Consulta relacionada",
    )

    @api.depends("resident_id", "title", "treatment_type", "start_date")
    def _compute_name(self):
        labels = dict(self._fields["treatment_type"].selection)
        for rec in self:
            if rec.resident_id and rec.title:
                t = labels.get(rec.treatment_type, "Tratamiento")
                ds = (
                    rec.start_date.strftime("%d/%m/%Y")
                    if rec.start_date
                    else ""
                )
                suffix = f" ({ds})" if ds else ""
                rec.name = f"{t} — {rec.title} — {rec.resident_id.name}{suffix}"
            else:
                rec.name = "Tratamiento"


class MedicalFollowup(models.Model):
    """Seguimiento planificado (revisiones, controles)."""

    _name = "cs.medical.followup"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Seguimiento médico"
    _order = "planned_date desc"

    name = fields.Char(string="Referencia", compute="_compute_name", store=True)
    resident_id = fields.Many2one(
        "cs.resident",
        string="Residente",
        required=True,
        index=True,
        tracking=True,
    )
    partner_id = fields.Many2one(
        "res.partner",
        related="resident_id.partner_id",
        store=True,
        readonly=True,
    )
    title = fields.Char(string="Motivo / tema seguimiento", required=True)
    planned_date = fields.Date(
        string="Próxima fecha revisión",
        tracking=True,
    )
    instructions = fields.Text(
        string="Indicaciones",
        help="Qué vigilar, medicación a revisar, derivaciones, etc.",
    )
    state = fields.Selection(
        [
            ("pending", "Pendiente"),
            ("done", "Realizado"),
            ("cancelled", "Cancelado"),
        ],
        string="Estado",
        default="pending",
        tracking=True,
    )
    completed_date = fields.Date(string="Fecha realización")
    coordinator_id = fields.Many2one(
        "cs.worker",
        string="Coordinador",
        domain=[("job_title", "in", ["médico", "enfermero"])],
    )
    consultation_id = fields.Many2one(
        "cs.medical.consultation",
        string="Consulta origen",
    )

    @api.depends("resident_id", "title", "planned_date")
    def _compute_name(self):
        for rec in self:
            if rec.resident_id and rec.title:
                ds = (
                    rec.planned_date.strftime("%d/%m/%Y")
                    if rec.planned_date
                    else "sin fecha"
                )
                rec.name = (
                    f"Seguimiento — {rec.title} — {rec.resident_id.name} ({ds})"
                )
            else:
                rec.name = "Seguimiento"
