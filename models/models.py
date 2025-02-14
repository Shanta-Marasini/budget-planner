# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class custom-addons/budget_planner(models.Model):
#     _name = 'custom-addons/budget_planner.custom-addons/budget_planner'
#     _description = 'custom-addons/budget_planner.custom-addons/budget_planner'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

