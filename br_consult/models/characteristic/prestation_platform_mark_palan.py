# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationPlatformMarkPalan(models.Model):
    _name = "prestation.platform.mark.palan"
    _description = "Prestation platform mark palan"

    name = fields.Char("Nom")
    sequence = fields.Integer('Séquence', default=10)
