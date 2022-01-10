# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationSuspendedPlatformSuspentionmark(models.Model):
    _name = "prestation.suspended.platform.suspension.mark"
    _description = "Prestation suspended platform suspension mark"

    name = fields.Char("Nom")
    sequence = fields.Integer('Séquence', default=10)
