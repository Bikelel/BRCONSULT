# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationLevageInstallationUse(models.Model):
    _name = "prestation.levage.installation.use"
    _description = "Prestation levage installation use"

    name = fields.Char("Name")
    sequence = fields.Integer('Séquence', default=10)
