from odoo import models, fields, api, exceptions

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'

    name = fields.Char(string="Title",required=True, default="New Property")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(string="Available From",copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer()
    garage = fields.Integer()
    garden = fields.Boolean()
    garden_area = fields.Integer(string='Garden Area (sqm)')
    active = fields.Boolean(default=False)
    state = fields.Selection(string='Status',selection=[
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled')
    ], default='new', copy=False)
    garden_orientation = fields.Selection(string='Type',selection=[
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ])
    property_type_id = fields.Many2one('estate.property.type')
    #property_type_id = fields.One2many('estate.property.type', 'property_ids', string='Property Type')
# res.partner: a partner is a physical or legal entity. It can be a company, an individual or even a contact address.
# res.partner: a partner is a physical or legal entity. 
# It can be a company, an individual or even a contact address.
# res.users: the users of the system. Users can be ‘internal’, i.e. they have access to the Odoo backend. 
# Or they can be ‘portal’, i.e. they cannot access the backend, 
# only the frontend (e.g. to access their previous orders in eCommerce).
    user_id = fields.Many2one('res.users', string='Salesperson', index=True, tracking=True, default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string=' ')
    total_area = fields.Integer(string='Total Area (sqm)', compute='_compute_total_area')
    best_price = fields.Float(string='Best Offer', compute='_compute_best_price')
    #Constraints in SQL
    _check_expected_price = models.Constraint('expected_price >= 0', 'The expected price must be a positive number.')
    _check_selling_price = models.Constraint('selling_price >= 0', 'The selling price must be a non-negative number.')
   #Model ordering
    _order = 'id desc' 


    #Constraints 
    @api.constrains("selling_price","expected_price")
    def _check_selling_price_expected_price(self):
        for record in self:
            if record.selling_price and record.selling_price < record.expected_price * 0.9:
                raise exceptions.ValidationError("The selling price cannot be lower than 90% of the expected price.")
    #Dependencies
    @api.depends("living_area","garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.mapped('offer_ids.price'))
            else:
                record.best_price = 0.0
#The ‘onchange’ mechanism provides a way for the client interface to update a form 
# without saving anything to the database whenever the user has filled in a field value.         
    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False
    
#By assigning type="object" to our button, the Odoo framework will execute 
# a Python method with name="action_do_something" on the given model.
    def action_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise exceptions.UserError("Canceled properties cannot be sold.")
            record.state = 'sold'
        return True
    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise exceptions.UserError("Sold properties cannot be canceled.")
            record.state = 'canceled'
        return True
# API model
#It is very important to always call super() to avoid breaking the flow. 
# There are only a few very specific cases where you don’t want to call it.
    @api.model
    def ondelete(self):
        for record in self:
            if record.state not in ['new', 'canceled']:
                raise exceptions.UserError("Only new or canceled properties can be deleted.")
        return super(EstateProperty, self).ondelete()
    