# -*- coding: utf-8 -*-
# from odoo import http


# class Custom-addons/budgetPlanner(http.Controller):
#     @http.route('/custom-addons/budget_planner/custom-addons/budget_planner', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom-addons/budget_planner/custom-addons/budget_planner/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom-addons/budget_planner.listing', {
#             'root': '/custom-addons/budget_planner/custom-addons/budget_planner',
#             'objects': http.request.env['custom-addons/budget_planner.custom-addons/budget_planner'].search([]),
#         })

#     @http.route('/custom-addons/budget_planner/custom-addons/budget_planner/objects/<model("custom-addons/budget_planner.custom-addons/budget_planner"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom-addons/budget_planner.object', {
#             'object': obj
#         })

