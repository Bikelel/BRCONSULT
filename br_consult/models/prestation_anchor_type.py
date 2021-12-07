# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationAnchorType(models.Model):
    _name = "prestation.anchor.type"
    _description = "Prestation anchor type"

    name = fields.Char("Name")
    sequence = fields.Integer('Séquence', default=10)
