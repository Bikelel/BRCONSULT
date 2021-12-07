# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationOtherDevice(models.Model):
    _name = "prestation.other.device"
    _description = "Prestation other device"

    name = fields.Char("Name")
    sequence = fields.Integer('Séquence', default=10)
