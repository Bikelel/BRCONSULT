# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PrestationScaffoldingCharacteristic(models.Model):
    _name = "prestation.scaffolding.characteristic"
    _description = "Prestation Scaffolding Characteristic"

    name = fields.Char("Name")
    prestation_id = fields.Many2one('prestation.prestation', 'Prestation')
    is_presence = fields.Boolean("Présence")
    length = fields.Float("Longeur")
    width = fields.Float("Largeur")
    height = fields.Float("Hauteur")
    surface = fields.Float("Surface (m2)", store=True, compute='_compute_surface')
    
    @api.depends('width', 'length')
    def _compute_surface(self):
        for rec in self:
            rec.surface = rec.width * rec.length