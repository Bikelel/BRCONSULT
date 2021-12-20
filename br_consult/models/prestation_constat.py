# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationConstat(models.Model):
    _name = "prestation.constat"
    _description = "Prestation Constat"

    name = fields.Char("Name")
    prestation_id = fields.Many2one('prestation.prestation', 'Prestation')
    type = fields.Selection(string="Type", related="verification_point_id.type", store=True)
    verification_point_id = fields.Many2one('prestation.verification.point', string="Point de vérification")
    observation_ids = fields.Many2many('prestation.observation', string="Observations/réserves" )
    reserve = fields.Text("Observations/réserves OLD")
    precision = fields.Text("Précisions")
    photo = fields.Binary("Photo")
    state = fields.Selection([
        ('to_lift', "A lever"),
        ('lifted', "Levée")], string="Statut")
    date = fields.Date('Date')
    
    @api.onchange('verification_point_id')
    def _onchange_verification_point_id(self):
        if self.verification_point_id:
            self.reserve = self.verification_point_id.observations