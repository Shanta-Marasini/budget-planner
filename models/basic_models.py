from odoo import api, fields, models, _
import datetime

class BudgetYears(models.Model):
    _name = 'budget.years'
    _description = 'Holds data for budgets of a year'

    def _get_year_selection(self):
            """Generate a list of years dynamically"""
            current_year = datetime.datetime.now().year
            return [(str(year), str(year)) for year in range(current_year - 10, current_year + 50)]

    name = fields.Selection(selection=_get_year_selection, string="Year", default=lambda self: str(datetime.datetime.now().year), required=True)    
    month_ids = fields.One2many('budget.months', 'year_id', string="Months")

class BudgetMonths(models.Model):
    _name = 'budget.months'
    _description = 'Holds data for budgets of a month'

    MONTH_SELECTION = [
        ('1', 'January'),
        ('2', 'February'),
        ('3', 'March'),
        ('4', 'April'),
        ('5', 'May'),
        ('6', 'June'),
        ('7', 'July'),
        ('8', 'August'),
        ('9', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December'),
    ]

    name = fields.Selection(MONTH_SELECTION, string="Month", required=True)
    year_id = fields.Many2one('budget.years', string="Year", ondelete="cascade")
