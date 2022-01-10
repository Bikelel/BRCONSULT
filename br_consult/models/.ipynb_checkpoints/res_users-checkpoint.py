# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Users(models.Model):
    _inherit = 'res.users'
    
    visa_user = fields.Binary('Visa inspecteur')
    is_inspector = fields.Boolean('Est un inspecteur')
    stage_ids = fields.Many2many("prestation.stage", string="Etapes Modifiable")