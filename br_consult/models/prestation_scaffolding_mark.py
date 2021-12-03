# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationScaffoldingMark(models.Model):
    _name = "prestation.scaffolding.mark"
    _description = "Prestation Scaffolding Mark"

    name = fields.Char("Name")
    prestation_id = fields.Many2one('prestation.prestation', 'Prestation')
    mark = fields.Selection([
        ('layher', 'Layher'),
        ('comabi', 'Comabi'),
        ('altrad_plettac', 'Altrad plettac'),
        ('other', 'Autre')], copy=False, string="Marque")
    
    other_mark = fields.Char("Autre marque")
    type = fields.Char("Type")
    height = fields.Float("Hauteur de niveau 1")
    height_max = fields.Float("Hauteur maxi (m2)")
    linear = fields.Float("Linéaire")
    inspected_surface = fields.Float("Surface inspectée (m2)", store=True, compute='_compute_inspected_surface')
    
    @api.depends('height_max', 'linear')
    def _compute_inspected_surface(self):
        for rec in self:
            rec.inspected_surface = rec.height_max * rec.linear