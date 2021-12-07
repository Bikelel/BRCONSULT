# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationScaffoldingClass(models.Model):
    _name = "prestation.scaffolding.class"
    _description = "Prestation scaffolding class"
    _order = "sequence"

    name = fields.Char("Name")   
    operating_overload = fields.Integer("Surcharge d'exploitation")
    sequence = fields.Integer('Séquence', default=1)
