# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationMark(models.Model):
    _name = "prestation.mark"
    _description = "Prestation mark"

    name = fields.Char("Name")
    sequence = fields.Integer('Séquence', default=10)
