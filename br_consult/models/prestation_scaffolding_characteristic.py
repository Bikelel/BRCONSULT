# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PrestationScaffoldingCharacteristic(models.Model):
    _name = "prestation.scaffolding.characteristic"
    _description = "Prestation Scaffolding Characteristic"

    name = fields.Char("Name")
    prestation_id = fields.Many2one('prestation.prestation', 'Prestation')
    characteristic_id = fields.Many2one('prestation.characteristic', string="Caractéristique")
    is_presence = fields.Selection([('yes', 'Oui'), ('no', 'Non')], string="Présence")
    length = fields.Float("Longeur")
    width = fields.Float("Largeur")
    height = fields.Float("Hauteur")
    surface = fields.Float("Surface (m2)", store=True, compute='_compute_surface')
    localisation_id = fields.Many2one('prestation.localisation', string = "Localisation")
    is_length = fields.Boolean("Is Longeur")
    is_width = fields.Boolean("Is Largeur")
    is_height = fields.Boolean("Is Hauteur")
    is_surface = fields.Boolean("Is Surface (m2)")
    
    @api.depends('width', 'length')
    def _compute_surface(self):
        for rec in self:
            if rec.width and rec.length and rec.is_surface:
                rec.surface = rec.width * rec.length
    
    @api.onchange('characteristic_id')
    def _onchange_characteristic_id(self):
        if self.characteristic_id:
            self.is_lenght = self.characteristic_id.is_lenght
            self.is_width = self.characteristic_id.is_width
            self.is_height = self.characteristic_id.is_height
            self.is_surface = self.characteristic_id.is_surface