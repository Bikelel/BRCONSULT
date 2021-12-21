# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationLocalisation(models.Model):
    _name = "prestation.localisation"
    _description = "Prestation localisation"

    name = fields.Char("Name")
    sequence = fields.Integer('Séquence', default=10)
