# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationSuspendedPlatformMark(models.Model):
    _name = "prestation.suspended.platform.mark"
    _description = "Prestation suspended platform mark"

    name = fields.Char("Nom")
    sequence = fields.Integer('Séquence', default=10)
