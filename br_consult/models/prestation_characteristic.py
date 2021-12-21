# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationCharacteristic(models.Model):
    _name = "prestation.characteristic"
    _description = "Prestation characteristic"

    name = fields.Char("Name", required=True)
    sequence = fields.Integer('Séquence', default=10)
    is_default = fields.Boolean("Remplir par défaut")
    is_length = fields.Boolean("Longeur", default=True)
    is_width = fields.Boolean("Largeur", default=True)
    is_height = fields.Boolean("Hauteur", default=True)
    is_surface = fields.Boolean("Surface (m2)", default=True)
