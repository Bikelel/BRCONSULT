# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationVerificationPoint(models.Model):
    _name = "prestation.verification.point"
    _description = "Prestation Verification Point"

    name = fields.Char("Nom", required=True)
    inspection_type = fields.Selection([
        ('echafaudage', 'Echafaudage'),
        ('levage', 'Levage'),
    ], copy=False, string="Type d'inspection", required=True)
    type = fields.Selection([
        ('adequacy_exam', "Examen d'adéquation"),
        ('assembly_exam', "Examen de montage et d'installation"),
        ('conservation_state_exam', "Examen de l'état de conservation"),
        ('good_functioning', "Examen de bon fonctionnement"),
        ('epreuve_statique', "Epreuves statiques"),
        ('epreuve_dynamique', "Epreuves dynamiques")], string="Type", required=True)
    observations = fields.Text("Observations old")
    observation_ids = fields.One2many("prestation.observation", 'verification_point_id', "Observations")
    installation_type = fields.Selection([
        ('PSE', 'Plateforme suspendue électrique'),
        ('PSM', 'Plateforme suspendue manuelle'),
        ('PWM', 'Plateforme de travail sur mat'),
        ('ASC', "Ascenseur de chantier"),
        ('PTR', 'Plateforme de transport'),
        ('MMA', 'Monte-matériaux'),
        ('TRE', 'Treuil'),
        ('PAE', 'Palan motorisé'),
        ('PAM', 'Palan manuel'),
        ('TUB', 'Echafaudage'),
    ], string="Type d'installation")
    
   