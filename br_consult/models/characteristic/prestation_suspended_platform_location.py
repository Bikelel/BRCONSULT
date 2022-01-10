# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationSuspendedPlatformLocatione(models.Model):
    _name = "prestation.suspended.platform.location"
    _description = "Prestation suspended platform location"

    name = fields.Char("Nom")
    sequence = fields.Integer('Séquence', default=10)
