# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationLevageMaxUse(models.Model):
    _name = "prestation.levage.max.use"
    _description = "Prestation levage Max use"

    name = fields.Char("Nom")
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
    ], string="Type d'installation")
    sequence = fields.Integer('Séquence', default=10)
