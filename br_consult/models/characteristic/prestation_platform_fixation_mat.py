# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationPlatformFixationMAT(models.Model):
    _name = "prestation.platform.fixation.mat"
    _description = "Prestation platform fixation MAT"

    name = fields.Char("Nom")
    sequence = fields.Integer('Séquence', default=10)
