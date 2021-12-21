# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationSuspendedPlatformAssembly(models.Model):
    _name = "prestation.suspended.platform.assembly"
    _description = "Prestation suspended platform assembly"

    name = fields.Char("Nom")
    sequence = fields.Integer('Séquence', default=10)
