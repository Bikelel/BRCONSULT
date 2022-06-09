# -*- coding: utf-8 -*-
# from odoo import http


# class Coordination(http.Controller):
#     @http.route('/coordination/coordination', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/coordination/coordination/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('coordination.listing', {
#             'root': '/coordination/coordination',
#             'objects': http.request.env['coordination.coordination'].search([]),
#         })

#     @http.route('/coordination/coordination/objects/<model("coordination.coordination"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('coordination.object', {
#             'object': obj
#         })
