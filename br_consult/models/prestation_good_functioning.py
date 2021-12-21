# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PrestationGoodFunctioning(models.Model):
    _name = "prestation.good.functioning"
    _description = "Prestation good functioning List"

    name = fields.Text("Nom", required=True)
    inspection_type = fields.Selection([
        #('echafaudage', 'Echafaudage'),
        ('levage', 'Levage'),
    ], string="Type d'inspection", required=True, default='levage')
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
    ], string="Type d'installation", required=True)
