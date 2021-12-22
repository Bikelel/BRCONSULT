# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationLevageCharacteristicSuspendedPlatform(models.Model):
    _name = "prestation.levage.characteristic.suspended.platform"
    _description = "Prestation levage characteristic suspended platform"

    name = fields.Char("N° de la plateforme suspendue")
    prestation_id = fields.Many2one('prestation.prestation', 'Prestation')
    height_platform = fields.Float("Hauteur plateforme")
    length_platform = fields.Float("Largeur plateforme")
    suspended_platform_location_id = fields.Many2one('prestation.suspended.platform.location', "Localisationde la plateforme suspendue")
    suspended_platform_access_id = fields.Many2one('prestation.suspended.platform.access', "Acces plateforme suspendue")
    suspended_platform_constitution_id = fields.Many2one('prestation.suspended.platform.constitution', "Constitution plateforme suspendue")
    suspended_platform_mark_id = fields.Many2one('prestation.suspended.platform.mark', "Marque plateforme suspendue")
    suspended_platform_assembly_id = fields.Many2one('prestation.suspended.platform.assembly', "Assemblage plateforme suspendue")
    suspended_platform_mark_treuil_id = fields.Many2one('prestation.suspended.platform.mark.treuil', "Marque treuil plateforme suspendue")
    type_treuil = fields.Char("Type de treuil")
    alimentation = fields.Selection([
        ('triphase', 'Triphase'),
        ('monophase', 'Monophase'),
    ], string="Alimentation")
    numero_treuil = fields.Char("N° treuil")
    capacity_treuil = fields.Char("Capacité treuil")
    is_taree = fields.Boolean("A une capacité tarée")
    capacity_taree = fields.Float("Capacité tarée")
    suspended_platform_cable_diameter_id = fields.Many2one('prestation.suspended.platform.cable.diameter', "Diametre des cables (en mm)")
    
    suspended_platform_suspension_id = fields.Many2one('prestation.suspended.platform.suspension', "Suspension par")
    suspended_platform_suspension_location_id = fields.Many2one('prestation.suspended.platform.suspension.location', "Localisation des suspensions")
    suspended_platform_suspension_mark_id = fields.Many2one('prestation.suspended.platform.suspension.mark', "Marque des suspensions")
    vertical_guide = fields.Selection([
        ('cable', 'Cables'),
        ('mat', 'Mat(s)'),
        ('sans_objet', 'Sans objet'),
    ], string="Guidage vertical")
    
    
    f1 = fields.Float('F1')
    f2 = fields.Float('F2')
    r1 = fields.Float('R1')
    r2 = fields.Float('R2')
    p1 = fields.Float('P1', compute='_compute_p1', store=True)
    p2 = fields.Float('P2', compute='_compute_p2', store=True)
    p1_lca = fields.Float('P1 LCA', compute='_compute_p1_lca', store=True)
    p2_lca = fields.Float('P2 LCA', compute='_compute_p2_lca', store=True)
    poids_p1 = fields.Selection([
        ('25', '25kg'),
        ('30', '30kg'),
    ], string="Poids")
    nombre_p1 = fields.Integer(string="Nombre")
    total_p1 = fields.Integer(string="Total", compute="_compute_total_p1", store='True')
    poids_p2 = fields.Selection([
        ('25', '25kg'),
        ('30', '30kg'),
    ], string="Poids")
    nombre_p2 = fields.Integer(string="Nombre")
    total_p2 = fields.Integer(string="Total", compute="_compute_total_p2", store='True')
    difference_p1 = fields.Float("P1", compute="_compute_differenceLest", store='True')
    difference_p2 = fields.Float("P2", compute="_compute_differenceLest", store='True')
    suspended_platform_cmu_id = fields.Many2one('prestation.suspended.platform.cmu', "CMU (en kg)")
    nb_personne_max = fields.Integer("Nombre de personnes maximum", related="suspended_platform_cmu_id.nb_personne_max")
    comment_cmu = fields.Html("Commentaire CMU")
    
    @api.depends('f1', 'r1','is_taree','capacity_taree')
    def _compute_p1_lca(self):
        for rec in self:
            if rec.r1 != 0.0:
                if rec.is_taree:
                    rec.p1_lca = round(((rec.f1 * rec.capacity_taree) / rec.r1) * 3.0, 2)
                else:
                    if rec.p1:
                        rec.p1_lca = rec.p1
                    else:
                        rec.p1_lca = 0.0
            else:
                rec.p1 = 0.0
    
    @api.depends('f2', 'r2','is_taree','capacity_taree')
    def _compute_p2_lca(self):
        for rec in self:
            if rec.r2 != 0.0:
                if rec.is_taree:
                    rec.p2_lca = round(((rec.f2 * rec.capacity_taree) / rec.r2) * 3.0, 2)
                else:
                    rec.p2_lca = rec.p2
            else:
                rec.p2 = 0.0
    
    @api.depends('f1', 'r1','capacity_taree')
    def _compute_p1(self):
        for rec in self:
            if rec.r1 != 0.0:
                rec.p1 = round(((rec.f1 * rec.capacity_taree) / rec.r1) * 3.0, 2)
            else:
                rec.p1 = 0.0

    @api.depends('f2', 'r2','capacity_taree')
    def _compute_p2(self):
        for rec in self:
            if rec.r2 != 0.0:
                rec.p2 = round(((rec.f2 * rec.capacity_taree) / rec.r2) * 3.0, 2)
            else:
                rec.p2 = 0.0
    
    @api.depends('poids_p1', 'nombre_p1')
    def _compute_total_p1(self):
        for rec in self:
            if rec.nombre_p1 != 0.0:
                rec.total_p1 = (int(rec.poids_p1) * rec.nombre_p1)
            else:
                rec.total_p1 = 0
    
    @api.depends('poids_p2', 'nombre_p2')
    def _compute_total_p2(self):
        for rec in self:
            if rec.nombre_p2 != 0.0:
                rec.total_p2 = (int(rec.poids_p2) * rec.nombre_p2)
            else:
                rec.total_p2 = False
    
    @api.depends('total_p1', 'p1_lca', 'total_p2', 'p2_lca')
    def _compute_differenceLest(self):
        for rec in self:
            rec.difference_p1 = rec.total_p1 - rec.p1_lca
            rec.difference_p2 = rec.total_p2 - rec.p2_lca 
