{
    'name': 'Centro Sanitario - Atención Médica',
    'version': '1.0.0',
    'category': 'Healthcare',
    'author': 'Equilibrium',
    'license': 'LGPL-3',
    'depends': ['base', 'mail', 'cs_resident', 'cs_patient_followup_forms'],
    'data': [
        'security/ir.model.access.csv',
        'views/medical_consultation_views.xml',
        'views/prescription_views.xml',
        'views/medical_history_views.xml',
        'views/resident_medical_views.xml',
    ],
    'installable': True,
    'application': False,
}
