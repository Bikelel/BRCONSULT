# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Event(models.Model):
    _inherit = 'calendar.event'
    
    prestation_id = fields.Many2one('prestation.prestation', 'Prestation')
          
