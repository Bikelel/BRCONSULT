# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationPlatformMark(models.Model):
    _name = "prestation.platform.mark"
    _description = "Prestation platform mark"

    name = fields.Char("Nom")
    sequence = fields.Integer('Séquence', default=10)
