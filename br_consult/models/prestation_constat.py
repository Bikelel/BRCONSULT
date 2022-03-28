# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class PrestationConstat(models.Model):
    _name = "prestation.constat"
    _description = "Prestation Constat"

    name = fields.Char("Nom", store=True, compute='compute_constat_name')
    prestation_id = fields.Many2one('prestation.prestation', 'Prestation')
    type = fields.Selection(string="Type", related="verification_point_id.type", store=True)
    verification_point_id = fields.Many2one('prestation.verification.point', string="Point de vérification")
    observation_ids = fields.Many2many('prestation.observation', string="Observations/réserves" )
    constat_observation_ids = fields.One2many('prestation.constat.observation', 'constat_id',string="Observations/réserves" )
    inspection_type = fields.Selection(related="prestation_id.inspection_type")
    installation_type = fields.Selection(related="prestation_id.installation_type")
    reserve = fields.Text("Observations/réserves OLD")
    precision = fields.Text("Précisions")
    photo = fields.Binary("Photo")
    state = fields.Selection([
        ('to_lift', "A lever"),
        ('lifted', "Levée")], string="Statut")
    date = fields.Date('Date')
    

    def action_show_details(self):
        view = self.env.ref('br_consult.view_prestation_constat_form')
        return {
            'name': _('%s') % self.name,
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_model': 'form',
            'res_model': 'prestation.constat',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'current',
            'res_id': self.id,
            'context': dict(self.env.context),
        }
    
    @api.depends('prestation_id', 'type', 'verification_point_id')
    def compute_constat_name(self):
        for line in self:
            nom = ""
            if line.prestation_id:
                nom += line.prestation_id.name + " "
            
            if line.type:
                nom += line.type + " "
           
            if line.verification_point_id:
                nom += line.verification_point_id.name + " "
            
            line.update({'name': nom})
            
        
    