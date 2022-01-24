# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationPlatformWindSpeedMax(models.Model):
    _name = "prestation.platform.wind.speed.max"
    _description = "Prestation platform Wind Speed Max"

    name = fields.Char("Nom")
    sequence = fields.Integer('Séquence', default=10)
