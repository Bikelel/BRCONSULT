# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Region(models.Model):
    _name = "res.partner.region"
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = 'Region'
    _order = 'name, id desc'
    
    name = fields.Char(string="Name", required=True)
    departement_ids = fields.One2many ('res.partner.departement', 'region_id', string="Departements")
