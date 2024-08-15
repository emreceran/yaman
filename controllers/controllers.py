# -*- coding: utf-8 -*-
# from odoo import http


# class Yaman(http.Controller):
#     @http.route('/yaman/yaman', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/yaman/yaman/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('yaman.listing', {
#             'root': '/yaman/yaman',
#             'objects': http.request.env['yaman.yaman'].search([]),
#         })

#     @http.route('/yaman/yaman/objects/<model("yaman.yaman"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('yaman.object', {
#             'object': obj
#         })
