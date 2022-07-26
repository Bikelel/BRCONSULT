# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Partner(models.Model):
    _inherit = 'res.partner'
    
    lastname_legal_representative = fields.Char("Nom du représentant Légal")
    firstname_legal_representative = fields.Char("Prénom du représentant Légal")
    email_legal_representative = fields.Char("Adresse électronique (e-mail)")
    phone_legal_representative = fields.Char("N° Téléphone (Fixe)")
    mobil_phone_legal_representative = fields.Char("N° Téléphone (Mobile)")
    siret = fields.Char('Numéro SIRET')
    is_mentor = fields.Boolean('Est un monteur')