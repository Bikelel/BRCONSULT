# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationWorkNature(models.Model):
    _name = "prestation.work.nature"
    _description = "Prestation work nature"

    name = fields.Char("Name")
    sequence = fields.Integer('Séquence', default=10)
