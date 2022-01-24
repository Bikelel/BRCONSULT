# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationPlatformSpeedUnit(models.Model):
    _name = "prestation.platform.speed.unit"
    _description = "Prestation platform Speed unit"

    name = fields.Char("Nom")
    sequence = fields.Integer('Séquence', default=10)
