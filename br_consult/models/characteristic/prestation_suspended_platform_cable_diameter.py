# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationSuspendedPlatformCableDiameter(models.Model):
    _name = "prestation.suspended.platform.cable.diameter"
    _description = "Prestation suspended platform cable diameter"

    name = fields.Char("Nom")
    sequence = fields.Integer('Séquence', default=10)
