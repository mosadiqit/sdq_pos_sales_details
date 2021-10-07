# -*- coding: utf-8 -*-
from odoo import http

# class SdqPosSalesDetails(http.Controller):
#     @http.route('/sdq_pos_sales_details/sdq_pos_sales_details/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sdq_pos_sales_details/sdq_pos_sales_details/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sdq_pos_sales_details.listing', {
#             'root': '/sdq_pos_sales_details/sdq_pos_sales_details',
#             'objects': http.request.env['sdq_pos_sales_details.sdq_pos_sales_details'].search([]),
#         })

#     @http.route('/sdq_pos_sales_details/sdq_pos_sales_details/objects/<model("sdq_pos_sales_details.sdq_pos_sales_details"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sdq_pos_sales_details.object', {
#             'object': obj
#         })