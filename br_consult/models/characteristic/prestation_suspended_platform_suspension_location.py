# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationSuspendedPlatformSuspentionLocation(models.Model):
    _name = "prestation.suspended.platform.suspension.location"
    _description = "Prestation suspended platform suspension location"

    name = fields.Char("Nom")
    sequence = fields.Integer('Séquence', default=10)
