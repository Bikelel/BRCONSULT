# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Prestation(models.Model):
    _inherit = 'prestation.prestation'
    
    event_id = fields.Many2one('calendar.event', 'Event', compute="sync_prestation_event", store="True")
    
    @api.depends('name', 'verification_date', 'user_id')
    def sync_prestation_event(self):

        if not self.event_id:
            self.create_prestation_calendar()


    def create_prestation_calendar(self):
        description = ""
        if self.inspection_type:
            description += "inspection_type : " + self.inspection_type + "\n"
        if self.installation_type:
            description += "installation_type : " + self.installation_type + "\n"
        if self.verification_type:
            description += "verification_type : " + self.verification_type + "\n"

        if self.partner_id:
            description += "Entreprise : " + self.partner_id.name + "\n"
            
        vals = {'name': self.name,
                'start': self.verification_date,
                'stop' : self.end_date_verification,
                'duration': self.prestation_duration,
                'location': self.site_address,
                'user_id': self.user_id.id,
                'description': description,
                'prestation_id' : self.id,
                
               }
        event_id = self.env['calendar.event'].sudo().create(vals)
        self.update({'event_id': event_id.id})
        
        
        
