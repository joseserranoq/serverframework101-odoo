from odoo import models, fields,api, exceptions
from datetime import timedelta
class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'

    price = fields.Float(string="Price", required=True)
    status = fields.Selection(string='Status', selection=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], default='pending', copy=False)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    create_date = fields.Date(string='Offer Date', readonly=True, default=fields.Date.today())
    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline', store=True, default=lambda self: fields.Date.add(fields.Date.today(), days=7))
    property_type_id = fields.Many2one(related='property_id.property_type_id', string='Property Type', store=True)
    #SQL Constraints
    _check_price = models.Constraint("CHECK(price > 0)","The offer price must be a positive number.")
    #model ordering
    _order = 'price desc'
    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = (record.create_date + timedelta(days=record.validity))
    #Inverse Fuction
    #the inverse method is called when saving the record, 
    # while the compute method is called at each change of its dependencies.
    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                delta = record.date_deadline - record.create_date
                record.validity = delta.days

    def accept_offer(self):
        for record in self:
            # Set all other offers for the same property to 'refused'
            other_offers = self.search([('property_id', '=', record.property_id.id), ('id', '!=', record.id)])
            other_offers.write({'status': 'refused'})
            # Set this offer to 'accepted'
            record.status = 'accepted'
            # Update the property's selling price and state
            record.property_id.selling_price = record.price
            record.property_id.state = 'offer_accepted'
            # Uodate the buyer of the property
            record.property_id.buyer_id = record.partner_id
        return True
    def refuse_offer(self):
        for record in self:
            record.status = 'refused'
        return True
    # API model
    @api.model
    def create(self, vals):
        # Call the super to create the offer
        offer = super(EstatePropertyOffer, self).create(vals)
        # Update the property state to 'offer_received' if it's currently 'new'
        #self.env[model_name].browse(value)
        property = offer.property_id
        if property.state == 'new':
            property.state = 'offer_received'
        elif property.offer_ids:
            best_offer = max(property.offer_ids.mapped('price'))
            if offer.price < best_offer:
                raise exceptions.ValidationError("The offer price must be higher than the existing offers.")
        return offer
    @api.model
    def ondelete(self):
        for record in self:
            if record.status == 'accepted':
                raise exceptions.UserError("Accepted offers cannot be deleted.")
        return super(EstatePropertyOffer, self).ondelete()
    
