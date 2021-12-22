# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationPlatformAssemblyMAT(models.Model):
    _name = "prestation.platform.assembly.mat"
    _description = "Prestation platform assembly MAT"

    name = fields.Char("Nom")
    sequence = fields.Integer('Séquence', default=10)
