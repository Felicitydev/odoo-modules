# -*- coding: utf-8 -*-
# from odoo import http


# class OdooInheritance(http.Controller):
#     @http.route('/odoo_inheritance/odoo_inheritance', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/odoo_inheritance/odoo_inheritance/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('odoo_inheritance.listing', {
#             'root': '/odoo_inheritance/odoo_inheritance',
#             'objects': http.request.env['odoo_inheritance.odoo_inheritance'].search([]),
#         })

#     @http.route('/odoo_inheritance/odoo_inheritance/objects/<model("odoo_inheritance.odoo_inheritance"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('odoo_inheritance.object', {
#             'object': obj
#         })
