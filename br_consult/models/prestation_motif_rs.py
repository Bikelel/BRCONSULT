# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationmotifRs(models.Model):
    _name = "prestation.motif.rs"
    _description = "Prestation motif rs"

    name = fields.Char("Name")
    sequence = fields.Integer('Séquence', default=10)
