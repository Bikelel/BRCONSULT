# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationConstatObservation(models.Model):
    _name = "prestation.constat.observation"
    _description = "Prestation Constat Observation"
    
    name = fields.Char("Name", related='observation_id.name')
    constat_id = fields.Many2one('prestation.constat', string='Constat')
    verification_point_id = fields.Many2one('prestation.verification.point', string="Point de vérification")
    type = fields.Selection(related="verification_point_id.type")
    observation_id = fields.Many2one('prestation.observation', string="Observations/réserves" )
    reserve = fields.Boolean("Reserve")
    color = fields.Integer("Couleur", compute = '_get_observation_color', store=True)
    
    @api.onchange('observation_id')
    def onchange_observation_id(self):
        for line in self:
            if line.observation_id:
                line.reserve = line.observation_id.reserve
    
    @api.depends('reserve')
    def _get_observation_color(self):
        for line in self:
            if line.reserve:
                line.color = 2
            else:
                line.color = 0