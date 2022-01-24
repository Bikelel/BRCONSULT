# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationSuspendedPlatformMarkTreuil(models.Model):
    _name = "prestation.suspended.platform.mark.treuil"
    _description = "Prestation suspended platform mark treuil"

    name = fields.Char("Nom")
    sequence = fields.Integer('Séquence', default=10)
