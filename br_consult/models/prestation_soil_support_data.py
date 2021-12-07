# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationSoilSupportSata(models.Model):
    _name = "prestation.soil.support.data"
    _description = "Prestation soil support data"

    name = fields.Char("Name")
    sequence = fields.Integer('Séquence', default=10)
