from odoo import models, fields, api, _
from datetime import date, datetime, time


class daily_purchase_product(models.Model):
    _name = 'daily_purchase_product'
    _description = 'Pos reporting'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='الدخول', readonly=True, default='الدخول')
    description = fields.Text(string='ملاحضات')
    document = fields.Binary(string='تفاصيل البيع الفعلية')
    date = fields.Date('التاريخ', track_visibility="always", required=True,
                       default=lambda self: fields.Date.to_string(date.today()), )
    capital = fields.Integer(string='راس المال')
    company_id = fields.Many2one(
        'res.company', readonly='True', string='نقطة البيع',
        default=lambda self: self.env['res.company']._company_default_get())
    purchase_lines = fields.One2many(comodel_name='purchase_products', inverse_name='product_id', string="Produits",
                                     copy=False)

    total_daily_purchase_product = fields.Float(string='البضاعة', readonly=True,
                                                compute='compute_total_daily_purchase_product')


    globaltotal_purchase = fields.Float(string='مجموع الدخول', compute='compute_globaltotal_purchase', readonly=True)
    outcome_amount = fields.Float(string=('مجموع الخروج'),compute='compute_outcome_amount')
    rest = fields.Float(compute='compute_rest_amount', string='الباقي')



    @api.depends('globaltotal_purchase', 'total_daily_purchase_product', 'capital')
    def compute_globaltotal_purchase(self):
        self.globaltotal_purchase = self.total_daily_purchase_product + self.capital

    @api.depends('rest', 'globaltotal_purchase', 'outcome_amount')
    def compute_rest_amount(self):
        self.rest = self.globaltotal_purchase - self.outcome_amount

    @api.depends('outcome_amount', 'total_daily_amount', 'total_daily_sales_product')
    def compute_outcome_amount(self):
        self.outcome_amount = self.total_daily_amount + self.total_daily_sales_product

    @api.onchange('purchase_lines')
    def compute_total_daily_purchase_product(self):
        self.total_daily_purchase_product = 0
        if self.purchase_lines:
            self.total_daily_purchase_product = sum(self.purchase_lines.mapped('price_total'))
            total_daily_purchase_product = fields.Float(string='البضاعة', readonly=True,
                                                        compute='compute_total_daily_purchase_product')

    # sales order lines

    total_daily_sales_product = fields.Float(string='مجموع المبيعات', readonly=True,
                                                compute='compute_total_daily_sales_product')
    sales_lines = fields.One2many(comodel_name='sales_products', inverse_name='product_id', string="Produits",
                                      copy=False)

    globaltotal_sales = fields.Float(string='مجموع المبيعات', compute='compute_total_daily_sales_product', readonly=True)


    @api.onchange('sales_lines')
    def compute_total_daily_sales_product(self):
        self.total_daily_sales_product = 0
        if self.sales_lines:
            self.total_daily_sales_product = sum(self.sales_lines.mapped('price_total'))




       # depenses order lines

    total_daily_depenses = fields.Float(string='مجموع المصاريف', readonly=True,
                                                compute='compute_total_daily_sales_product')
    depenses_lines = fields.One2many(comodel_name='depenses', inverse_name='product_id', string="المصاريف",
                                      copy=False)

    globaltotal_depenses = fields.Float(string='مجموع المصاريف', compute='compute_total_daily_depenses', readonly=True)


    @api.onchange('depenses_lines')
    def compute_total_daily_depenses(self):
        self.total_daily_depenses = 0
        if self.depenses_lines:
            self.total_daily_depenses = sum(self.depenses_lines.mapped('price_total'))






       # final calcul

    total_daily_amount = fields.Float(string='الحساب النهائي', readonly=True,
                                                compute='compute_total_daily_amount')
    amount_lines = fields.One2many(comodel_name='amount', inverse_name='product_id', string="الحساب النهائي",
                                      copy=False)

    globaltotal_amount = fields.Float(string='الحساب النهائي', compute='compute_total_daily_depenses', readonly=True)


    @api.onchange('amount_lines')
    def compute_total_daily_amount(self):
        self.total_daily_amount = 0
        if self.amount_lines:
            self.total_daily_amount = sum(self.amount_lines.mapped('price_total'))






class purchase_products(models.Model):
    _name = 'purchase_products'
    _description = 'Pos purchase reporting'

    product_id = fields.Many2one(
        "product.product",
        string="المنتجات")
    qty = fields.Float(string="العدد")
    # uom_id = fields.Many2one(
    #     "uom.uom", string="Unit of Measure",
    #     required=True)
    price_unit = fields.Float('السعر', required=True, default=0.0)
    price_tax = fields.Float(string='Total Tax', store=True)
    tax_id = fields.Float(string='Taxes', store=True)
    price_total = fields.Float(string='المجموع', readonly=True, store=True, compute='_compute_subtotal')

    # price_subtotal = fields.Float(string='Total HT', readonly=True, store=True, compute='_compute_total')
    # project_unit = fields.Char(string='Project Unit')
    # project_unit_description = fields.Char(string='Déscription')
    # project_unit_location = fields.Text(string='Adresse')

    @api.onchange("product_id")
    def _onchange_product_id(self):
        self.name = self.product_id.name
        self.uom_id = self.product_id.uom_id.id
        # self.name = self.product_id.name

    @api.depends('qty', 'price_unit', 'price_total', 'tax_id')
    def _compute_subtotal(self):
        for each in self:
            each.price_total = 0
            tax_id = 0
            if each.tax_id:
                tax_id = (each.price_unit * each.qty) * each.tax_id / 100
            each.price_total = tax_id + (each.qty * each.price_unit)

    # @api.depends('qty', 'price_unit', 'price_total')
    # def _compute_total(self):
    #     for each in self:
    #         each.price_total = 0
    #         tax_id = 0
    #         each.price_total = each.qty * each.price_unit


class sales_products(models.Model):
    _name = 'sales_products'
    _description = 'Pos sales reporting'

    product_id = fields.Many2one(
        "product.product",
        string="المنتجات")
    qty = fields.Float(string="العدد")
    # uom_id = fields.Many2one(
    #     "uom.uom", string="Unit of Measure",
    #     required=True)
    price_unit = fields.Float('السعر', required=True, default=0.0)
    price_tax = fields.Float(string='Total Tax', store=True)
    tax_id = fields.Float(string='Taxes', store=True)
    price_total = fields.Float(string='المجموع', readonly=True, store=True, compute='_compute_subtotal')

    # price_subtotal = fields.Float(string='Total HT', readonly=True, store=True, compute='_compute_total')
    # project_unit = fields.Char(string='Project Unit')
    # project_unit_description = fields.Char(string='Déscription')
    # project_unit_location = fields.Text(string='Adresse')

    @api.onchange("product_id")
    def _onchange_product_id(self):
        self.name = self.product_id.name
        self.uom_id = self.product_id.uom_id.id
        # self.name = self.product_id.name

    @api.depends('qty', 'price_unit', 'price_total', 'tax_id')
    def _compute_subtotal(self):
        for each in self:
            each.price_total = 0
            tax_id = 0
            if each.tax_id:
                tax_id = (each.price_unit * each.qty) * each.tax_id / 100
            each.price_total = tax_id + (each.qty * each.price_unit)

    # @api.depends('qty', 'price_unit', 'price_total')
    # def _compute_total(self):
    #     for each in self:
    #         each.price_total = 0
    #         tax_id = 0
    #         each.price_total = each.qty * each.price_unit

class sales_products(models.Model):
    _name = 'depenses'
    _description = 'depenses'

    product_id = fields.Many2one(
        "product.product",
        string="المنتجات")
    qty = fields.Float(string="العدد")
    # uom_id = fields.Many2one(
    #     "uom.uom", string="Unit of Measure",
    #     required=True)
    price_unit = fields.Float('السعر', required=True, default=0.0)
    price_tax = fields.Float(string='Total Tax', store=True)
    tax_id = fields.Float(string='Taxes', store=True)
    price_total = fields.Float(string='المجموع', readonly=True, store=True, compute='_compute_subtotal')

    # price_subtotal = fields.Float(string='Total HT', readonly=True, store=True, compute='_compute_total')
    # project_unit = fields.Char(string='Project Unit')
    # project_unit_description = fields.Char(string='Déscription')
    # project_unit_location = fields.Text(string='Adresse')

    @api.onchange("product_id")
    def _onchange_product_id(self):
        self.name = self.product_id.name
        self.uom_id = self.product_id.uom_id.id
        # self.name = self.product_id.name

    @api.depends('qty', 'price_unit', 'price_total', 'tax_id')
    def _compute_subtotal(self):
        for each in self:
            each.price_total = 0
            tax_id = 0
            if each.tax_id:
                tax_id = (each.price_unit * each.qty) * each.tax_id / 100
            each.price_total = tax_id + (each.qty * each.price_unit)


class sales_products(models.Model):
    _name = 'amount'
    _description = 'depenses'

    product_id = fields.Many2one(
        "product.product",
        string="المنتجات")
    qty = fields.Float(string="العدد")
    price_unit = fields.Float('السعر', required=True, default=0.0)
    price_tax = fields.Float(string='Total Tax', store=True)
    tax_id = fields.Float(string='Taxes', store=True)
    price_total = fields.Float(string='المجموع', readonly=True, store=True, compute='_compute_subtotal')


    @api.onchange("product_id")
    def _onchange_product_id(self):
        self.name = self.product_id.name
        self.uom_id = self.product_id.uom_id.id
        # self.name = self.product_id.name

    @api.depends('qty', 'price_unit', 'price_total', 'tax_id')
    def _compute_subtotal(self):
        for each in self:
            each.price_total = 0
            tax_id = 0
            if each.tax_id:
                tax_id = (each.price_unit * each.qty) * each.tax_id / 100
            each.price_total = tax_id + (each.qty * each.price_unit)
