# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationSuspendedPlatformConstitution(models.Model):
    _name = "prestation.suspended.platform.constitution"
    _description = "Prestation suspended platform constitution"

    name = fields.Char("Nom")
    sequence = fields.Integer('Séquence', default=10)
