# -*- coding: utf-8 -*-
###############################################################################
#
#   Copyright (C) 2004-today OpenERP SA (<http://www.openerp.com>)
#   Copyright (C) 2016-today Geminate Consultancy Services (<http://geminatecs.com>).
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from odoo import models, api
import datetime
from datetime import timedelta, MAXYEAR
from dateutil import rrule
from dateutil.relativedelta import relativedelta
import time
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, pycompat

class Prestation(models.Model):
    _inherit = 'prestation.prestation'
    
    
    # @api.multi
    def get_prestation_values(self,user_id):
        partner = self.env.user.partner_id
        prestations = self.env['prestation.prestation'].search([('message_partner_ids', 'child_of', [partner.commercial_partner_id.id]),('state', 'in', ['sent', 'cancel'])])
        myLabels  =[]
        myData_dict = {}
        myData =[]
        res ={}
        if prestations:
            for order in prestations:
                
                if order.partner_id.name in myData_dict:
                    myData_dict[order.partner_id.name] = myData_dict[order.partner_id.name]  + order.amount_total
                else:
    #                 myLabels.append(order.partner_id.name)
                    myData_dict.update({order.partner_id.name : order.amount_total})
                    
            for data in myData_dict:
                myData.append(myData_dict[data])
                myLabels.append(data)
            res.update({
                        'my_data':myData,
                        'my_labels':myLabels
                        })
            return res
        return False
    
    # @api.multi
    def get_customer_prestation_cancelled_values(self, user_id):
        partner = self.env.user.partner_id
        prestations = self.env['prestation.prestation'].search([('message_partner_ids', 'child_of', [partner.commercial_partner_id.id]),('state', 'in', ['cancel'])])
        myLabels  =[]
        myData_dict = {}
        myData =[]
        res ={}
        if prestations:
            for order in prestations:
                
                if order.partner_id.name in myData_dict:
                    myData_dict[order.partner_id.name] = myData_dict[order.partner_id.name]  + order.amount_total
                else:
                    myData_dict.update({order.partner_id.name : order.amount_total})
                    
            for data in myData_dict:
                myData.append(myData_dict[data])
                myLabels.append(data)
            res.update({
                        'my_data':myData,
                        'my_labels':myLabels
                        })
            return res
        return False
    
    # @api.multi
    def get_prestation_cancelled_values(self, user_id):
        partner = self.env.user.partner_id
        month_list = ['January','February','March','April','May','June','July','August','September','October','November','December']
        prestations = self.env['prestation.prestation'].search([('message_partner_ids', 'child_of', [partner.commercial_partner_id.id]),('state', 'in', ['cancel'])],order='date_order asc')
        myLabels  =[]
        myData = []
        res ={}
        date_dict = {}
        if prestations:
            for order in prestations:
                is_copy = False
                date_value = (order.date_order)
                date_child_dict = {'month':date_value.month,'year':date_value.year,'total': order.amount_total}
                for items in date_dict:
                    if date_dict[items]['month'] == date_value.month and date_dict[items]['year'] == date_value.year:
                        is_copy = True
                        date_dict[items].update({'month':date_value.month,'year':date_value.year,'total': order.amount_total + date_dict[items]['total']})
                if not is_copy:
                    date_dict.update({str(date_child_dict['month']) + '-' + str(date_child_dict['year']):date_child_dict})
            
            for vals in date_dict:
                myLabels.append(str(month_list[date_dict[vals]['month'] - 1]) + str(date_dict[vals]['year']))
                myData.append(str(date_dict[vals]['total']))
            res.update({
                        'my_data':myData,
                        'my_labels':myLabels
                        })
            return res
        else :
            return False
    
    # @api.multi
    def get_prestation_month_values(self,user_id):
        partner = self.env.user.partner_id
        month_list = ['January','February','March','April','May','June','July','August','September','October','November','December']
        prestations = self.env['prestation.prestation'].search([('message_partner_ids', 'child_of', [partner.commercial_partner_id.id]),('state', 'in', ['sent', 'cancel'])],order='date_order asc')
        myLabels  =[]
        myData = []
        res ={}
        date_dict = {}
        if prestations:
            for order in prestations:
                is_copy = False
                date_value = (order.date_order)
                date_child_dict = {'month':date_value.month,'year':date_value.year,'total': order.amount_total}
                for items in date_dict:
                    if date_dict[items]['month'] == date_value.month and date_dict[items]['year'] == date_value.year:
                        is_copy = True
                        date_dict[items].update({'month':date_value.month,'year':date_value.year,'total': order.amount_total + date_dict[items]['total']})
                if not is_copy:
                    date_dict.update({str(date_child_dict['month']) + '-' + str(date_child_dict['year']):date_child_dict})
            
            for vals in date_dict:
                myLabels.append(str(month_list[date_dict[vals]['month'] - 1]) + str(date_dict[vals]['year']))
                myData.append(str(date_dict[vals]['total']))
            res.update({
                        'my_data':myData,
                        'my_labels':myLabels
                        })
            return res
        else :
            return False
    
    
    # @api.multi
    def get_prestation_values_by_date(self,user_id,start_date,end_date,filter):
        partner = self.env.user.partner_id
        month_list = ['January','February','March','April','May','June','July','August','September','October','November','December']
        prestations = self.env['prestation.prestation'].search([('message_partner_ids', 'child_of', [partner.commercial_partner_id.id]),('state', 'in', ['sent', 'cancel']),('date_order','>=',start_date),('date_order','<=',end_date)],order='date_order asc')
        myLabels  =[]
        myData = []
        res ={}
        date_dict = {}
        if prestations:
            if filter == 'month':
                for order in prestations:
                    is_copy = False
                    date_value = (order.date_order)
                    date_child_dict = {'month':date_value.month,'year':date_value.year,'total': order.amount_total}
                    for items in date_dict:
                        if date_dict[items]['month'] == date_value.month and date_dict[items]['year'] == date_value.year:
                            is_copy = True
                            date_dict[items].update({'month':date_value.month,'year':date_value.year,'total': order.amount_total + date_dict[items]['total']})
                    if not is_copy:
                        date_dict.update({str(date_child_dict['month']) + '-' + str(date_child_dict['year']):date_child_dict})
                
                for vals in date_dict:
                    myLabels.append(str(month_list[date_dict[vals]['month'] - 1]) + str(date_dict[vals]['year']))
                    myData.append(str(date_dict[vals]['total']))
                res.update({
                            'my_data':myData,
                            'my_labels':myLabels
                            })
                return res
        else :
            return False
    
    # @api.multi
    def get_prestation_cancelled_values_month(self,user_id,start_date,end_date):
        partner = self.env.user.partner_id
        month_list = ['January','February','March','April','May','June','July','August','September','October','November','December']
        prestations = self.env['prestation.prestation'].search([('message_partner_ids', 'child_of', [partner.commercial_partner_id.id]),('state', 'in', ['cancel']),('date_order','>=',start_date),('date_order','<=',end_date)],order='date_order asc')
        myLabels  =[]
        myData = []
        res ={}
        date_dict = {}
        if prestations:
            for order in prestations:
                is_copy = False
                date_value = (order.date_order)
                date_child_dict = {'month':date_value.month,'year':date_value.year,'total': order.amount_total}
                for items in date_dict:
                    if date_dict[items]['month'] == date_value.month and date_dict[items]['year'] == date_value.year:
                        is_copy = True
                        date_dict[items].update({'month':date_value.month,'year':date_value.year,'total': order.amount_total + date_dict[items]['total']})
                if not is_copy:
                    date_dict.update({str(date_child_dict['month']) + '-' + str(date_child_dict['year']):date_child_dict})
            
            for vals in date_dict:
                myLabels.append(str(month_list[date_dict[vals]['month'] - 1]) + str(date_dict[vals]['year']))
                myData.append(str(date_dict[vals]['total']))
            res.update({
                        'my_data':myData,
                        'my_labels':myLabels
                        })
            return res
        else :
            return False
    
    # @api.multi
    def get_prestation_values_by_year(self,user_id,start_date,end_date,filter):
        partner = self.env.user.partner_id
        prestations = self.env['prestation.prestation'].search([('message_partner_ids', 'child_of', [partner.commercial_partner_id.id]),('state', 'in', ['sent', 'cancel']),('date_order','>=',start_date),('date_order','<=',end_date)],order='date_order asc')
        myLabels  =[]
        myData = []
        res ={}
        date_dict = {}
        if prestations:
            if filter == 'year':
                for order in prestations:
                    is_copy = False
                    date_value = (order.date_order)
                    date_child_dict = {'year':date_value.year,'total': order.amount_total}
                    for items in date_dict:
                        if date_dict[items]['year'] == date_value.year:
                            is_copy = True
                            date_dict[items].update({'year':date_value.year,'total': order.amount_total + date_dict[items]['total']})
                    if not is_copy:
                        date_dict.update({str(date_child_dict['year']):date_child_dict})
                for vals in date_dict:
                    myLabels.append(date_dict[vals]['year'])
                    myData.append(date_dict[vals]['total'])
                res.update({
                            'my_data':myData,
                            'my_labels':myLabels
                            })
            return res
        else :
            return False

    # @api.multi
    def get_prestation_cancelled_values_year(self,user_id,start_date,end_date):
        partner = self.env.user.partner_id
        prestations = self.env['prestation.prestation'].search([('message_partner_ids', 'child_of', [partner.commercial_partner_id.id]),('state', 'in', ['cancel']),('date_order','>=',start_date),('date_order','<=',end_date)],order='date_order asc')
        myLabels  =[]
        myData = []
        res ={}
        date_dict = {}
        if prestations:
            for order in prestations:
                is_copy = False
                date_value = (order.date_order)
                date_child_dict = {'year':date_value.year,'total': order.amount_total}
                for items in date_dict:
                    if date_dict[items]['year'] == date_value.year:
                        is_copy = True
                        date_dict[items].update({'year':date_value.year,'total': order.amount_total + date_dict[items]['total']})
                if not is_copy:
                    date_dict.update({str(date_child_dict['year']):date_child_dict})
            for vals in date_dict:
                myLabels.append(date_dict[vals]['year'])
                myData.append(date_dict[vals]['total'])
            res.update({
                        'my_data':myData,
                        'my_labels':myLabels
                        })
            return res
        else :
            return False
