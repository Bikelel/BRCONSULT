# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Users(models.Model):
    _inherit = 'res.users'
    
    visa_user_id = fields.Binary('Visa inspecteur')