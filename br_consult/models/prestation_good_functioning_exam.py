# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PrestationGoodFunctioningExam(models.Model):
    _name = "prestation.good.functioning.exam"
    _description = "Prestation good functioning exam"

    name = fields.Char("Nom")
    good_functioning_id = fields.Many2one("prestation.good.functioning", string ="Element du bon fonctionnement") 
    inspection_type = fields.Selection(related="good_functioning_id.inspection_type")
    installation_type = fields.Selection(related="good_functioning_id.installation_type")
    prestation_id = fields.Many2one("prestation.prestation", string="Prestation")
    opinion = fields.Selection([('yes', 'Satisfaisant'), 
                                ('no', 'Non satisfaisant'),
                                ('wo', 'Sans Objet')], string="Avis")

