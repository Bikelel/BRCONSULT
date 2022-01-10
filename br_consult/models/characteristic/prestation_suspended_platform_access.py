# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationSuspendedPlatformAccesse(models.Model):
    _name = "prestation.suspended.platform.access"
    _description = "Prestation suspended platform access"

    name = fields.Char("Nom")
    sequence = fields.Integer('Séquence', default=10)
