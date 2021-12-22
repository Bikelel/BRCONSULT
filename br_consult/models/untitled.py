# -*- coding: utf-8 -*-
import base64

from odoo import api, fields, models, tools, _
from datetime import datetime, timedelta
from datetime import date
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
# import datetime
from dateutil.relativedelta import relativedelta

import logging
_logger = logging.getLogger(__name__)



class plateforme_levage(models.Model):
    _name = "plateforme.levage"

    prestation_id = fields.Many2one('prestation.prestation')

    state = fields.Char(related='prestation_id.state')


    """Plateforme"""
    name = fields.Integer("N° de la plateforme suspendue")
    hauteur = fields.Float("Hauteur d'elevation")
    localisation_plateforme = fields.Selection([
        ('rue', 'Façade rue'),
        ('cour', 'Façade cour'),
        ('arriere', 'Façade arrière'),
        ('pignon', 'Pignon'),
        ('autre', 'Autre'),
    ], string="LOCALISATION DE LA PLATE FORME SUSPENDUE")
    localisation_plateforme_autre = fields.Char("AUTRE")
    mission_contract_ref = fields.Char(
        'La mission est réalisée conformément au contrat réf')
    mission_type = fields.Selection([
        ('1', 'MISE EN SERVICE'),
        ('2', 'REMISE EN SERVICE'),
        ('3', 'VISITE PÉRIODIQUE'),
    ], string="Il s’agit d’une mission de")

    longueur_plateforme = fields.Float("LONGUEUR DE LA PLATE FORME SUSPENDUE (EN M)")
    acces_plateforme = fields.Selection([
        ('sol', 'Sol, RDC'),
        ('terrasse', 'Terrasse'),
        ('sapine', 'Sapine'),
        ('autre', 'Autre'),
    ], string="ACCES PLATE FORME")
    acces_plateforme_autre = fields.Char("AUTRE")

    def _get_acces_plateforme_value(self):
        for record in self:
            if record.acces_plateforme:
                if record.acces_plateforme == 'autre':
                    record.acces_plateforme_value = record.acces_plateforme
                else:
                    record.acces_plateforme_value = dict(record._fields['acces_plateforme'].selection).get(
                        record.acces_plateforme)

    acces_plateforme_value = fields.Char(string="", compute=_get_acces_plateforme_value)

    constitution = fields.Selection([
        ('alu', "Aluminium"),
        ('bois', 'Bois'),
        ('autre', 'Autre'),
    ], string="CONSTITUTION")
    constitution_autre = fields.Char('AUTRE')

    def _get_constitution_value(self):
        for record in self:
            if record.constitution:
                if record.constitution == 'autre':
                    record.constitution_value = record.constitution
                else:
                    record.constitution_value = dict(record._fields['constitution'].selection).get(record.constitution)

    constitution_value = fields.Char(string="", compute=_get_constitution_value)

    plateforme_image_1 = fields.Binary('Image 1'.upper())
    plateforme_image_2 = fields.Binary('Image 2'.upper())
    plateforme_image_3 = fields.Binary('Image 3'.upper())
    plateforme_image_4 = fields.Binary('Image 4'.upper())
    plateforme_image_5 = fields.Binary('Image 5'.upper())

    """Modules"""
    assemblage = fields.Selection([
        ('groupille', "Goupilles"),
        ('boulon', "Boulons"),
        ('autre', 'Autre'),
    ], string="ASSEMBLAGE")
    assemblage_autre = fields.Char('AUTRE')

    def _get_assemblage_value(self):
        for record in self:
            if record.assemblage:
                if record.assemblage == 'autre':
                    record.assemblage_value = record.assemblage
                else:
                    record.assemblage_value = dict(record._fields['assemblage'].selection).get(record.assemblage)

    assemblage_value = fields.Char(string="", compute=_get_assemblage_value)

    marque_module = fields.Selection([
        ('tractel', 'Tractel'),
        ('fixator', 'Fixator'),
        ('comabi', 'Comabi'),
        ('altrex', 'Altrex'),
        ('autre', 'Autre'),
    ], string="MARQUE DES MODULES")
    marque_module_autre = fields.Char("AUTRE")

    def _get_marque_module_value(self):
        for record in self:
            if record.marque_module:
                if record.marque_module == 'autre':
                    record.marque_module_value = record.marque_module
                else:
                    record.marque_module_value = dict(record._fields['marque_module'].selection).get(
                        record.marque_module)

    marque_module_value = fields.Char(string="", compute=_get_marque_module_value)

    module_image_1 = fields.Binary('Image 1'.upper())
    module_image_2 = fields.Binary('Image 2'.upper())
    module_image_3 = fields.Binary('Image 3'.upper())
    module_image_4 = fields.Binary('Image 4'.upper())
    module_image_5 = fields.Binary('Image 5'.upper())

    """Treuil"""
    marque_treuil = fields.Selection([
        ('tractel', 'Tractel'),
        ('fixator', 'Fixator'),
        ('powerclimber', 'Powerclimber'),
        ('autre', 'Autre'),
    ], string="MARQUE DES TREUILS")
    marque_treuil_autre = fields.Char("AUTRE")

    def _get_marque_treuil_value(self):
        for record in self:
            if record.marque_treuil:
                if record.marque_treuil == 'autre':
                    record.marque_treuil_value = record.marque_treuil
                else:
                    record.marque_treuil_value = dict(record._fields['marque_treuil'].selection).get(
                        record.marque_treuil)

    marque_treuil_value = fields.Char(string="", compute=_get_marque_treuil_value)

    type_treuil = fields.Char("TYPE DE TREUIL")
    alimentation = fields.Selection([
        ('triphase', "Triphase"),
        ('monophase', "Monophase"),
    ], string="Alimentation".upper())

    def _get_alimentation_value(self):
        for record in self:
            if record.alimentation:
                if record.alimentation == 'autre':
                    record.alimentation_value = record.alimentation
                else:
                    record.alimentation_value = dict(record._fields['alimentation'].selection).get(record.alimentation)

    alimentation_value = fields.Char(string="", compute=_get_alimentation_value)

    numero_treuil = fields.Char("N° DES TREUILS")
    capacite_treuil = fields.Integer("CAPACITE NOMINALE DES TREUILS")
    diametre_cable = fields.Selection([
        ('8', '8mm'),
        ('8.3', '8.3mm'),
        ('9', '9mm'),
        ('autre', 'Autre'),
    ], string="DIAMETRE DES CABLES (EN MM)")
    diametre_cable_autre = fields.Float("AUTRE")
    suspension_par = fields.Selection([
        ('PL', 'Poutres lestées'),
        ('PS', 'Poutres spittées'),
        ('PA', 'Pinces d\'acrotère'),
        ('autre', 'Autre'),
    ], string="SUSPENSION PAR")
    suspension_par_autre = fields.Char("AUTRE")
    def _get_diametre_cable_value(self):
        for record in self:
            if record.diametre_cable:
                if record.diametre_cable == 'autre':
                    record.diametre_cable_value = record.diametre_cable
                else:
                    record.diametre_cable_value = dict(record._fields['diametre_cable'].selection).get(
                        record.diametre_cable)

    diametre_cable_value = fields.Char(string="", compute=_get_diametre_cable_value)

    taree = fields.Selection([
        ('taree', 'Tarée:'),
        ('sansobjet', 'Sans objet'),
    ], string='Capacite taree'.upper())
    #taree_saisie = fields.Char("Taree".upper())
    taree_saisie = fields.Float("Taree".upper())

    def _get_taree_value(self):
        for record in self:
            if record.taree:
                if record.taree == 'taree':
                    record.taree_value = record.taree
                else:
                    record.taree_value = dict(record._fields['taree'].selection).get(record.taree)

    taree_value = fields.Char(string="AUTRE", compute=_get_taree_value)

    treuil_image_1 = fields.Binary('Image 1'.upper())
    treuil_image_2 = fields.Binary('Image 2'.upper())
    treuil_image_3 = fields.Binary('Image 3'.upper())
    treuil_image_4 = fields.Binary('Image 4'.upper())
    treuil_image_5 = fields.Binary('Image 5'.upper())

    """Suspension/Poutres"""
    suspension = fields.Selection([
        ('lestee', 'Poutres lestées'),
        ('spittee', 'Poutres spittées'),
        ('acrotere', "Pinces d'acrotère"),
        ('autre', 'Autre'),
    ], string="SUSPENSION PAR")
    suspension_autre = fields.Char("AUTRE")

    def _get_suspension_value(self):
        for record in self:
            if record.suspension:
                if record.suspension == 'autre':
                    record.suspension_value = record.suspension
                else:
                    record.suspension_value = dict(record._fields['suspension'].selection).get(record.suspension)

    suspension_value = fields.Char(string="", compute=_get_suspension_value)

    localisation_suspension = fields.Selection([
        ('terrasse', 'Toiture terrasse'),
        ('balcon', 'Balcon'),
        ('autre', 'Autre')
    ], string="LOCALISATION DES SUSPENSIONS")
    localisation_suspension_autre = fields.Char("AUTRE")

    def _get_localisation_suspension_value(self):
        for record in self:
            if record.localisation_suspension:
                if record.localisation_suspension == 'autre':
                    record.localisation_suspension_value = record.localisation_suspension
                else:
                    record.localisation_suspension_value = dict(
                        record._fields['localisation_suspension'].selection).get(record.localisation_suspension)

    localisation_suspension_value = fields.Char(string="", compute=_get_localisation_suspension_value)

    marque_suspension = fields.Selection([
        ('tractel', 'Tractel'),
        ('fixator', 'Fixator'),
        ('powerclimber', 'Powerclimber'),
        ('skyclimber', 'Skyclimber'),
        ('autre', 'Autre'),
    ], string="MARQUE DES SUSPENSIONS")
    marque_suspension_autre = fields.Char("AUTRE")

    def _get_marque_suspension_value(self):
        for record in self:
            if record.marque_suspension:
                if record.marque_suspension == 'autre':
                    record.marque_suspension_value = record.marque_suspension
                else:
                    record.marque_suspension_value = dict(record._fields['marque_suspension'].selection).get(
                        record.marque_suspension)

    marque_suspension_value = fields.Char(string="", compute=_get_marque_suspension_value)

    """ Calcul du lest """

    '''lest calcule'''

    @api.onchange('f1', 'r1','capacite_treuil','taree_saisie','taree')
    @api.one
    def _calcul_p1_lca(self):
        for rec in self:
            if rec.r1 != 0.0:
                if rec.taree == 'taree':
                    rec.p1_lca = round(((rec.f1 * rec.taree_saisie) / rec.r1) * 3.0, 2)
                else:
                    rec.p1_lca = rec.p1
            else:
                rec.p1 = False

    @api.onchange('f2', 'r2','capacite_treuil','taree_saisie','taree')
    @api.one
    def _calcul_p2_lca(self):
        for rec in self:
            if rec.r2 != 0.0:
                if rec.taree == 'taree':
                    rec.p2_lca = round(((rec.f2 * rec.taree_saisie) / rec.r2) * 3.0, 2)
                else:
                    rec.p2_lca = rec.p2
            else:
                rec.p2 = False

    p1_lca = fields.Float('P1', compute=_calcul_p1_lca)
    p2_lca = fields.Float('P2', compute=_calcul_p2_lca)

    ''' calcul cotes'''


    @api.onchange('f1', 'r1','capacite_treuil')
    @api.one
    def _calcul_p1(self):
        for rec in self:
            if rec.r1 != 0.0:
                rec.p1 = round(((rec.f1 * rec.capacite_treuil) / rec.r1) * 3.0, 2)
            else:
                rec.p1 = False

    @api.onchange('f2', 'r2','capacite_treuil')
    @api.one
    def _calcul_p2(self):
        for rec in self:
            if rec.r2 != 0.0:
                rec.p2 = round(((rec.f2 * rec.capacite_treuil) / rec.r2) * 3.0, 2)
            else:
                rec.p2 = False


    p1 = fields.Float('P1', compute=_calcul_p1)
    f1 = fields.Float('F1')
    r1 = fields.Float('R1')
    p2 = fields.Float('P2', compute=_calcul_p2)
    f2 = fields.Float('F2')
    r2 = fields.Float('R2')


    """ Fin calcul du lest """

    """lest constate """
    """P1"""

    poids_p1 = fields.Selection([
        ('25', '25kg'),
        ('30', '30kg'),
        
    ], string="Poids")

    nombre_p1 = fields.Integer(string="Nombre")
    total_p1 = fields.Integer(string="Total", compute="calcul")

    @api.onchange('poids_p1', 'nombre_p1')
    @api.one
    def calcul(self):
        for rec in self:
                    if rec.nombre_p1 != 0.0:
                        rec.total_p1 = (int(rec.poids_p1) * rec.nombre_p1)
                    else:
                        rec.total_p1 = False



    """P2""" 
    poids_p2 = fields.Selection([
        ('25', '25kg'),
        ('30', '30kg'),
        
    ], string="Poids")
    nombre_p2 = fields.Integer(string="Nombre")
    total_p2 = fields.Integer(string="Total", compute="calcul_p2")

    @api.onchange('poids_p2', 'nombre_p2')
    @api.one
    def calcul_p2(self):
        for rec in self:
                    if rec.nombre_p2 != 0.0:
                        rec.total_p2 = (int(rec.poids_p2) * rec.nombre_p2)
                    else:
                        rec.total_p2 = False

    """Difference lest"""
    difference_p1 = fields.Float("P1", compute="differenceLest")
    difference_p2 = fields.Float("P2", compute="differenceLest")


    @api.onchange('total_p1', 'p1_lca', 'total_p2', 'p2_lca')
    @api.one
    def differenceLest(self):
        for rec in self:
            rec.difference_p1 = rec.total_p1 - rec.p1_lca
            rec.difference_p2 = rec.total_p2 - rec.p2_lca 
                
    '''alterte observation'''
    alerte_observation = fields.Text(string=" ", compute="alerte")

    @api.onchange('difference_p1', 'difference_p2')
    @api.one
    def alerte(self):
        for rec in self:
                    if rec.difference_p1 < 0 and rec.difference_p2 < 0:
                        rec.alerte_observation = "Compléter observations rubrique examen de montage "
                    else:
                        rec.alerte_observation = ""
    lest_constate = fields.Char("LEST CONSTATE (EN KG)")
    guidage_vertical = fields.Selection([
        ('cables', "CÂBLES"),
        ('mats', "MÂTS"),
        ('sans objet','SANS OBJET'),
    ], string='GUIDAGE VERTICAL')

    def _get_guidage_vertical_value(self):
        for record in self:
            if record.guidage_vertical:
                if record.guidage_vertical == 'autre':
                    record.guidage_vertical_value = record.guidage_vertical
                else:
                    record.guidage_vertical_value = dict(record._fields['guidage_vertical'].selection).get(
                        record.guidage_vertical)

    guidage_vertical_value = fields.Char(string="", compute=_get_guidage_vertical_value)

    assemblage_suspension = fields.Selection([
        ('goupille', 'Goupilles'),
        ('boulon', 'Boulons'),
        ('autre', 'Autre'),
    ], string="ASSEMBLAGE DES ELEMENTS DE SUSPENSION")

    assemblage_suspension_autre = fields.Char('AUTRE')

    def _get_assemblage_suspension_value(self):
        for record in self:
            if record.assemblage_suspension:
                if record.assemblage_suspension == 'autre':
                    record.aassemblage_suspension_value = record.assemblage_suspension
                else:
                    record.assemblage_suspension_value = dict(record._fields['assemblage'].selection).get(record.assemblage_suspension)

    assemblage_suspension_value = fields.Char(string="", compute=_get_assemblage_suspension_value)

    suspension_poutre_image_1 = fields.Binary('Image 1'.upper())
    suspension_poutre_image_2 = fields.Binary('Image 2'.upper())
    suspension_poutre_image_3 = fields.Binary('Image 3'.upper())
    suspension_poutre_image_4 = fields.Binary('Image 4'.upper())
    suspension_poutre_image_5 = fields.Binary('Image 5'.upper())

    """CHARGE MAX D'UTILISATION"""

    @api.onchange('cmu')
    @api.one
    def onchange_cmu(self):
        correspondance = {
            '120': 1,
            '240': 2,
            '320': 3,
            '400': 4,
            '480': 5,
            'autre': 0,
        }
        for rec in self:
            rec.nb_personne_max = correspondance[rec.cmu or 'autre']

    cmu = fields.Selection([
        ('120', '120 kg'),
        ('240', '240 kg'),
        ('320', '320 kg'),
        ('400', '400 kg'),
        ('480', '480 kg'),
        ('autre', 'Autre'),
    ], string="CMU (EN KG)")
    cmu_autre = fields.Float('AUTRE')

    def _get_cmu_value(self):
        for record in self:
            if record.cmu:
                if record.cmu == 'autre':
                    record.cmu_value = record.cmu
                else:
                    record.cmu_value = dict(record._fields['cmu'].selection).get(record.cmu)

    cmu_value = fields.Char(string="", compute=_get_cmu_value)

    nb_personne_max = fields.Integer("Nombre de personnes maximum".upper(), compute=onchange_cmu)
    nb_personne_max_autre = fields.Integer("Nombre de personnes maximum".upper())
    commentaire_cmu = fields.Text(string="COMMENTAIRE")
    
