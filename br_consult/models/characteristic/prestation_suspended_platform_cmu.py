# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationSuspendedPlatformCMU(models.Model):
    _name = "prestation.suspended.platform.cmu"
    _description = "Prestation suspended platform CMU"

    name = fields.Char("Nom")
    nb_personne_max = fields.Integer("Nombre de personnes maximum")
    sequence = fields.Integer('Séquence', default=10)
