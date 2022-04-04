# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationConstatObservation(models.Model):
    _name = "prestation.constat.observation"
    _description = "Prestation Constat Observation"
    _rec_name = 'observation_id'
    
    name = fields.Char("Name")
    constat_id = fields.Many2one('prestation.constat', string='Constat')
    verification_point_id = fields.Many2one('prestation.verification.point', string="Point de vérification")
    type = fields.Selection(related="verification_point_id.type")
    observation_id = fields.Many2one('prestation.observation', string="Observations/réserves" )
    reserve = fields.Boolean("Reserve")
    color = fields.Integer("Couleur", default=0)
    
    @api.onchange('observation_id')
    def onchange_observation_id(self):
        for line in self:
            if line.observation_id:
                line.reserve = line.observation_id.reserve
                line.name = line.observation_id.name
    
    @api.onchange('reserve')
    def _get_observation_color(self):
        for line in self:
            if line.reserve:
                line.color = 2
            else:
                line.color = 0