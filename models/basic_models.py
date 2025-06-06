from odoo import api, fields, models, _
import datetime

class BudgetYears(models.Model):
    _name = 'budget.years'
    _description = 'Holds data for budgets of a year'

    @api.model
    def _get_year_selection(self):
        """Generate a list of years dynamically from current year to next 30 years"""
        current_year = datetime.datetime.now().year
        return [(str(year), str(year)) for year in range(current_year, current_year + 30)]

    name = fields.Selection(selection=_get_year_selection, string="Year", required=True)    
    month_ids = fields.One2many('budget.months', 'year_id', string="Months")
    expense_ids = fields.One2many('budget.expense', 'year_id', string="Expense Lines")
    income_ids = fields.One2many('budget.income', 'year_id', string="Income Lines")

    
    currency_id = fields.Many2one('res.currency', string='Currency', store=True, compute='_compute_currency_id')

    monthly_average_income = fields.Monetary(
        string='Monthly Average Income',
        compute='_compute_income_expense', store=True,
        currency_field="currency_id"
    )

    monthly_average_expense = fields.Monetary(
        string='Monthly Average Expense',
        compute='_compute_income_expense', store=True,
        currency_field="currency_id"
    )

    _sql_constraints = [
    ('unique_year', 'unique(name)', 'The Year must be unique!')
    ]

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
            record.monthly_average_income = record.year_income / len(record.month_ids) if record.year_income else 0.0
            record.monthly_average_expense = record.year_expense / len(record.month_ids) if record.year_expense else 0.0
        

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

    _sql_constraints = [
    ('unique_month', 'unique(year_id, name)', 'The Month must be unique!')
    ]

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
    _rec_name = 'category_id'

    # name = fields.Selection(MONTH_SELECTION, string="Month", required=True)
    year_id = fields.Many2one('budget.years', string="Year", ondelete="cascade")
    month_id = fields.Many2one('budget.months', string="Month", ondelete="cascade", domain="[('year_id', '=', year_id)]")
    category_id = fields.Many2one('budget.category', string="Category", required=True, domain="[('category_type', '=', 'income')]")
    sub_category_id = fields.Many2one('budget.sub.category', string="Sub Category", domain="[('category_id', '=', category_id)]") 


    date = fields.Date(string="Date")
    description = fields.Text(string="Description")
    status = fields.Selection(
        selection=[
            ('planned', 'Planned'),
            ('done', 'Done'),
            ],
        default='planned',
        string="Status",
    )
    
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, compute='_compute_currency_id')

    @api.depends_context('company')
    def _compute_currency_id(self):
        self.currency_id = self.env.company.currency_id

    line_income = fields.Monetary(
        string='Amount',
        currency_field="currency_id"
    )

    @api.onchange('category_id')
    def _onchange_category_id(self):
        """Reset sub_category_id when category_id is changed."""
        self.sub_category_id = False



class BudgetExpense(models.Model):
    _name = 'budget.expense'
    _description = 'Holds data for expense'
    _rec_name = 'category_id'

    # name = fields.Selection(MONTH_SELECTION, string="Month", required=True)
    year_id = fields.Many2one('budget.years', string="Year", ondelete="cascade")
    month_id = fields.Many2one('budget.months', string="Month", ondelete="cascade", domain="[('year_id', '=', year_id)]")
    category_id = fields.Many2one('budget.category', string="Category", required=True, domain="[('category_type', '=', 'expense')]")
    sub_category_id = fields.Many2one('budget.sub.category', string="Sub Category", domain="[('category_id', '=', category_id)]")    
    expense_line_items = fields.One2many('budget.expense.items', 'expense_id', string="Expense Items")
    date = fields.Date(string="Date")
    place = fields.Many2one('budget.place', string="Place")
    units = fields.Integer(string="Units")
    description = fields.Text(string="Description")
    status = fields.Selection(
        selection=[
            ('planned', 'Planned'),
            ('done', 'Done'),
            ],
        default='planned',
        string="Status",
    )


    currency_id = fields.Many2one('res.currency', string='Currency', required=True, compute='_compute_currency_id')

    @api.depends_context('company')
    def _compute_currency_id(self):
        self.currency_id = self.env.company.currency_id

    line_expense = fields.Monetary(
        string='Amount',
        currency_field="currency_id"
    )

    @api.onchange('category_id')
    def _onchange_category_id(self):
        """Reset sub_category_id when category_id is changed."""
        self.sub_category_id = False

    # @api.onchange('year_id', 'month_id')
    # def _onchange_date(self):
    #     """Ensure the date is within the selected year and month."""
    #     if self.year_id and self.month_id and self.date:
    #         # Get the first and last day of the selected month and year
    #         first_day = datetime.datetime(self.year_id.name, self.month_id.name, 1)
    #         last_day = first_day.replace(month=self.month_id.name % 12 + 1, day=1) - dateime.timedelta(days=1)
            
    #         # If the date is not in range, raise a warning instead of resetting the date
    #         if not (first_day <= self.date <= last_day):
    #             # Raise a warning message to the user
    #             raise UserError(
    #                 f"The date {self.date} is not within the selected month ({self.month_id.name}) "
    #                 f"for the year {self.year_id.name}. Please select a valid date."
    #             )


class BudgetExpenseItems(models.Model):
    _name = 'budget.expense.items'
    _description = 'Holds data for expense items'

    name = fields.Char(string="Item", required=True)
    expense_id = fields.Many2one('budget.expense', string="Expense Line", ondelete="cascade")
    expense_id_category = fields.Many2one(
        'budget.category',
        string="Expense Category",
        related="expense_id.category_id",
        store=True,  # Store the value in the database
        readonly=True  # Make it non-editable
    )
    sub_category_id = fields.Many2one('budget.sub.category', string="Sub Category", domain="[('category_id', '=', expense_id_category)]") 

    currency_id = fields.Many2one('res.currency', string='Currency', required=True, compute='_compute_currency_id')

    @api.depends_context('company')
    def _compute_currency_id(self):
        self.currency_id = self.env.company.currency_id

    item_expense = fields.Monetary(
        string='Amount',
        currency_field="currency_id"
    )



class BudgetCategory(models.Model):
    _name = 'budget.category'
    _description = 'Holds data for categories of income and expenses'

    name = fields.Char(string="Category Name")    
    category_type = fields.Selection(selection=[("income", "Income"), ("expense", "Expense")], string="Type")
    sub_category_ids = fields.One2many('budget.sub.category', 'category_id', string="Sub Categories")


class BudgetSubCategory(models.Model):
    _name = 'budget.sub.category'
    _description = 'Holds data for sub categories of income and expenses'

    name = fields.Char(string="Name")    
    category_id = fields.Many2one('budget.category', string="Category", ondelete="cascade")

class BudgetPlace(models.Model):
    _name = 'budget.place'
    _description = 'Holds data for places'

    name = fields.Char(string="Name")    
