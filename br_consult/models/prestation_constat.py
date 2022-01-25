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
    inspection_type = fields.Selection(related="prestation_id.inspection_type")
    installation_type = fields.Selection(related="prestation_id.installation_type")
    reserve = fields.Text("Observations/réserves OLD")
    precision = fields.Text("Précisions")
    photo = fields.Binary("Photo")
    state = fields.Selection([
        ('to_lift', "A lever"),
        ('lifted', "Levée")], string="Statut")
    date = fields.Date('Date')
    