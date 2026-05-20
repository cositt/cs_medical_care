from odoo import models, fields


class MedicalTreatmentLine(models.Model):
    _name = "cs.medical.treatment.line"
    _description = "Línea de tratamiento"
    _order = "sequence, id"

    treatment_id = fields.Many2one(
        "cs.medical.treatment",
        string="Tratamiento",
        required=True,
        ondelete="cascade",
        index=True,
    )
    sequence = fields.Integer(default=10)
    description = fields.Char(string="Descripción / indicación", required=True)
    dose = fields.Char(string="Dosis / cantidad")
    frequency = fields.Char(string="Pauta / frecuencia")
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
    )
    notes = fields.Text(string="Observaciones")
