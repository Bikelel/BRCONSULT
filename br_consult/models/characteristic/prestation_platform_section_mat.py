# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationPlatformSectionMAT(models.Model):
    _name = "prestation.platform.section.mat"
    _description = "Prestation platform Section MAT"

    name = fields.Char("Nom")
    sequence = fields.Integer('Séquence', default=10)
