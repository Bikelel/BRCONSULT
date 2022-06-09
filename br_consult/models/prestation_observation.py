# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationObservation(models.Model):
    _name = "prestation.observation"
    _description = "Prestation Observation"

    name = fields.Char("Name", required=True)
    verification_point_id = fields.Many2one('prestation.verification.point', string="Point de vérification")
    type = fields.Selection(related="verification_point_id.type", store=True)
    reserve = fields.Boolean("Reserve")
    temp_save = fields.Boolean("Enregisrement temporaire")
    color = fields.Integer("Couleur", compute = '_get_observation_color', store=True)
    
    @api.depends('reserve')
    def _get_observation_color(self):
        for line in self:
            if line.reserve:
                line.color = 2
            else:
                line.color = 0