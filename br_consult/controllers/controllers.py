# -*- coding: utf-8 -*-
# from odoo import http


# class BrConsult(http.Controller):
#     @http.route('/br_consult/br_consult', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/br_consult/br_consult/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('br_consult.listing', {
#             'root': '/br_consult/br_consult',
#             'objects': http.request.env['br_consult.br_consult'].search([]),
#         })

#     @http.route('/br_consult/br_consult/objects/<model("br_consult.br_consult"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('br_consult.object', {
#             'object': obj
#         })
