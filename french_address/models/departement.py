# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Departement(models.Model):
    _name = "res.partner.departement"
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = 'Departement'
    _order = 'code, id desc'
    
    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    region_id = fields.Many2one ('res.partner.region', string="Region")
    
