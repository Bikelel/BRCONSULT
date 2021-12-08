# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationApproachFloorWidth(models.Model):
    _name = "prestation.approach.floor.width"
    _description = "Prestation approach floor width"

    name = fields.Char("Name")
    sequence = fields.Integer('Séquence', default=10)
