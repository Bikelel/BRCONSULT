# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PrestationConservationState(models.Model):
    _name = "prestation.conservation.state"
    _description = "Prestation conservation state List"

    name = fields.Html("Nom", required=True)
    inspection_type = fields.Selection([
        ('echafaudage', 'Echafaudage'),
        ('levage', 'Levage'),
    ], string="Type d'inspection", required=True)
    installation_type = fields.Selection([
        ('PSE', 'Plateforme suspendue électrique'),
        ('PSM', 'Plateforme suspendue manuelle'),
        ('PWM', 'Plateforme de travail sur mat'),
        ('ASC', "Ascenseur de chantier"),
        ('PTR', 'Plateforme de transport'),
        ('MMA', 'Monte-matériaux'),
        ('TRE', 'Treuil'),
        ('PAE', 'Palant motorisé'),
        ('PAM', 'Palant manuel'),
        ('TUB', 'Echafaudage'),
    ], string="Type d'installation")
