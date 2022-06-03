# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationMessageLabel(models.Model):
    _name = "prestation.message.label"
    _description = "Prestation Message Label"
    _rec_name = 'name'

    name = fields.Char("Nom de l'étape", required=True, translate=True)
    inspection_type = fields.Selection([
        ('echafaudage', 'Echafaudage'),
        ('levage', 'Levage'),
    ], copy=False, string="Type d'inspection")
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
    ], copy=False, string="Type d'installation")
    verification_type = fields.Selection([
        ('MS', 'Mise en service'),
        ('RS', 'Remise en service'),
        ('VP', 'Vérification périodique'),
    ], copy=False, string="Type de vérification")
    date = fields.Date("Date d'application", default=fields.Date.today())
    description = fields.Text("Code de l'article")
