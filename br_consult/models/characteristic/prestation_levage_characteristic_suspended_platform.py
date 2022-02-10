# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PrestationLevageCharacteristicSuspendedPlatform(models.Model):
    _name = "prestation.levage.characteristic.suspended.platform"
    _description = "Prestation levage characteristic suspended platform"

    name = fields.Char("N° de la plateforme suspendue",required=True)
    prestation_id = fields.Many2one('prestation.prestation', 'Prestation')
    installation_type = fields.Selection(related="prestation_id.installation_type")
    suspended_platform_location_id = fields.Many2one('prestation.suspended.platform.location', "Localisation de la plateforme")
    height_platform = fields.Float("Hauteur d'élévation (en mètre)")
    length_platform = fields.Float("Longeur de la plateforme")
    
    suspended_platform_access_id = fields.Many2one('prestation.suspended.platform.access', "Accès à la plateforme")
    suspended_platform_constitution_id = fields.Many2one('prestation.suspended.platform.constitution', "Constitution")
    suspended_platform_mark_id = fields.Many2one('prestation.suspended.platform.mark', "Marque de la plateforme")
    suspended_platform_assembly_id = fields.Many2one('prestation.suspended.platform.assembly', "Assemblage des modules")
    suspended_platform_mark_treuil_id = fields.Many2one('prestation.suspended.platform.mark.treuil', "Marque des treuils")
    type_treuil = fields.Char("Type des treuils")
    alimentation = fields.Selection([
        ('triphase', 'Triphase'),
        ('monophase', 'Monophase'),
    ], string="Alimentation")
    numero_treuil = fields.Char("N° des treuils")
    capacity_treuil = fields.Integer("Capacité nominale des treuils")
    is_taree = fields.Boolean("A une capacité tarée")
    capacity_taree = fields.Float("Capacité tarée")
    suspended_platform_cable_diameter_id = fields.Many2one('prestation.suspended.platform.cable.diameter', "Diamètre des câbles (en mm)")
    
#     suspended_platform_suspension_id = fields.Many2one('prestation.suspended.platform.suspension', "Suspension par")
    suspension_by = fields.Selection([
        ('p_lest', 'Poutres lestées'),
        ('p_spit', 'Poutres spittées'),
        ('pince', "Pince d'acrotère"),
        ('other', 'Autre'),
    ], string="Suspension par")
    other_suspension_by = fields.Char("Autre Suspension par")
    suspended_platform_suspension_location_id = fields.Many2one('prestation.suspended.platform.suspension.location', "Localisation des suspensions")
    suspended_platform_suspension_assembly_id = fields.Many2one('prestation.suspended.platform.assembly', "Assemblage des éléments de suspension")
    
    suspended_platform_suspension_mark_id = fields.Many2one('prestation.suspended.platform.suspension.mark', "Marque des suspensions")
    vertical_guide = fields.Selection([
        ('cable', 'Câbles'),
        ('mat', 'Mât(s)'),
        ('sans_objet', 'Sans objet'),
    ], string="Guidage vertical")
    
    
    f1 = fields.Float('F1')
    f2 = fields.Float('F2')
    r1 = fields.Float('R1')
    r2 = fields.Float('R2')
    p1_lca = fields.Float('P1 LCA', compute='_compute_p1_lca', store=True)
    p2_lca = fields.Float('P2 LCA', compute='_compute_p2_lca', store=True)
    poids_p1 = fields.Selection([
        ('25', '25kg'),
        ('30', '30kg'),
    ], string="Poids P1")
    nombre_p1 = fields.Integer(string="Nombre P1")
    total_p1 = fields.Integer(string="Total P1", compute="_compute_total_p1", store='True')
    poids_p2 = fields.Selection([
        ('25', '25kg'),
        ('30', '30kg'),
    ], string="Poids P2")
    nombre_p2 = fields.Integer(string="Nombre P2")
    total_p2 = fields.Integer(string="Total P2", compute="_compute_total_p2", store='True')
    difference_p1 = fields.Float("P1", compute="_compute_differenceLest", store='True')
    difference_p2 = fields.Float("P2", compute="_compute_differenceLest", store='True')
    suspended_platform_cmu_id = fields.Many2one('prestation.suspended.platform.cmu', "CMU (en kg)")
    nb_personne_max = fields.Integer("Nombre de personnes maximum", related="suspended_platform_cmu_id.nb_personne_max")
    comment_cmu = fields.Html("Commentaire CMU")
    sign_difference_p1 = fields.Boolean("Signe de différence P1", compute="_compute_differenceLest", store=True)
    sign_difference_p2 = fields.Boolean("Signe de différence P2", compute="_compute_differenceLest", store=True)
    
    @api.depends('f1', 'r1','is_taree','capacity_taree', 'capacity_treuil')
    def _compute_p1_lca(self):
        for rec in self:
            if rec.r1 != 0.0:
                if rec.is_taree:
                    rec.p1_lca = round(((rec.f1 * rec.capacity_taree) / rec.r1) * 3.0, 2)
                else:
                    rec.p1_lca = round(((rec.f1 * rec.capacity_treuil) / rec.r1) * 3.0, 2)
            else:
                rec.p1_lca = 0.0
    
    @api.depends('f2', 'r2','is_taree','capacity_taree', 'capacity_treuil')
    def _compute_p2_lca(self):
        for rec in self:
            if rec.r2 != 0.0:
                if rec.is_taree:
                    rec.p2_lca = round(((rec.f2 * rec.capacity_taree) / rec.r2) * 3.0, 2)
                else:
                    rec.p2_lca = round(((rec.f2 * rec.capacity_treuil) / rec.r2) * 3.0, 2)
            else:
                rec.p2_lca = 0.0
    
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
            
            if rec.difference_p1 >= 0:
                rec.sign_difference_p1 = True
            else:
                rec.sign_difference_p1 = False
            
            if rec.difference_p2 >= 0:
                rec.sign_difference_p2 = True
            else:
                rec.sign_difference_p2 = False
                
