# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationSuspendedPlatformSuspention(models.Model):
    _name = "prestation.suspended.platform.suspension"
    _description = "Prestation suspended platform suspension"

    name = fields.Char("Nom")
    sequence = fields.Integer('Séquence', default=10)
