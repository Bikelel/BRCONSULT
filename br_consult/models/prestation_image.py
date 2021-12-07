# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationImage(models.Model):
    _name = "prestation.image"
    _description = "Prestation Image"

    name = fields.Char("Name")
    prestation_id = fields.Many2one('prestation.prestation', 'Prestation')
    image = fields.Binary("Image")
