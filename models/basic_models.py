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
    expense_ids = fields.One2many('budget.expense', 'year_id', string="Expense Lines")
    income_ids = fields.One2many('budget.income', 'year_id', string="Income Lines")

    
    currency_id = fields.Many2one('res.currency', string='Currency', store=True, compute='_compute_currency_id')

    # todo @api.depends('company')
    def _compute_currency_id(self):
        self.currency_id = self.env.company.currency_id

    year_expense = fields.Monetary(
        string='Expense',
        compute='_compute_income_expense', store=True,
        currency_field="currency_id"
    )

    year_income = fields.Monetary(
        string='Income',
        compute='_compute_income_expense', store=True,
        currency_field="currency_id"
    )

    @api.depends('month_ids.month_income', 'month_ids.month_expense')  
    def _compute_income_expense(self):
        for record in self:
            record.year_income = sum(record.month_ids.mapped('month_income')) if record.month_ids else 0.0
            record.year_expense = sum(record.month_ids.mapped('month_expense')) if record.month_ids else 0.0
        

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
    expense_ids = fields.One2many('budget.expense', 'month_id', string="Expense Lines")
    income_ids = fields.One2many('budget.income', 'month_id', string="Income Lines")


    currency_id = fields.Many2one('res.currency', string='Currency', required=True, compute='_compute_currency_id')

    @api.depends_context('company')
    def _compute_currency_id(self):
        self.currency_id = self.env.company.currency_id

    month_expense = fields.Monetary(
        string='Expense',
        compute='_compute_income_expense', store=True,
        currency_field="currency_id"
    )

    month_income = fields.Monetary(
        string='Income',
        compute='_compute_income_expense', store=True,
        currency_field="currency_id"
    )

    @api.depends('income_ids.line_income', 'expense_ids.line_expense')  
    def _compute_income_expense(self):
        for record in self:
            record.month_income = sum(record.income_ids.mapped('line_income')) if record.income_ids else 0.0
            record.month_expense = sum(record.expense_ids.mapped('line_expense')) if record.expense_ids else 0.0
    

class BudgetIncome(models.Model):
    _name = 'budget.income'
    _description = 'Holds data for income'

    # name = fields.Selection(MONTH_SELECTION, string="Month", required=True)
    year_id = fields.Many2one('budget.years', string="Year", ondelete="cascade")
    month_id = fields.Many2one('budget.months', string="Month", ondelete="cascade")
    category_id = fields.Many2one('budget.category', string="Category", domain="[('category_type', '=', 'income')]")


    date = fields.Date(string="Date")
    #to dos
    # source 
    # owner
    # status = selection planned /received
    
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, compute='_compute_currency_id')

    @api.depends_context('company')
    def _compute_currency_id(self):
        self.currency_id = self.env.company.currency_id

    line_income = fields.Monetary(
        string='Amount',
        currency_field="currency_id"
    )



class BudgetExpense(models.Model):
    _name = 'budget.expense'
    _description = 'Holds data for expense'

    # name = fields.Selection(MONTH_SELECTION, string="Month", required=True)
    year_id = fields.Many2one('budget.years', string="Year", ondelete="cascade")
    month_id = fields.Many2one('budget.months', string="Month", ondelete="cascade")
    category_id = fields.Many2one('budget.category', string="Category", domain="[('category_type', '=', 'expense')]")
    date = fields.Date(string="Date")


    currency_id = fields.Many2one('res.currency', string='Currency', required=True, compute='_compute_currency_id')

    @api.depends_context('company')
    def _compute_currency_id(self):
        self.currency_id = self.env.company.currency_id

    line_expense = fields.Monetary(
        string='Amount',
        currency_field="currency_id"
    )


class BudgetYears(models.Model):
    _name = 'budget.category'
    _description = 'Holds data for categories of income and expenses'

    name = fields.Char(string="Category Name")    
    category_type = fields.Selection(selection=[("income", "Income"), ("expense", "Expense")], string="Type")
