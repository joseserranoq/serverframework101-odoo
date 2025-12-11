from odoo import models, fields,exceptions, api

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Real Estate Property Type'

    name = fields.Char(string="Type Name", required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string="Properties")
    sequence = fields.Integer('Sequence', default=1)
    offer_ids = fields.One2many(related='property_ids.offer_ids', string='Offers', readonly=True)
    offer_count = fields.Integer(string='Offer Count', compute='_compute_offer_count')
    #SQL constraint
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'The property type name must be unique.')
    ]
    #model Ordering
    _order = 'name asc'
    # @api.constrains('name')
    # def _check_unique_name(self):
    #     for record in self:
    #         existing_type = self.search([('name', '=', record.name), ('id', '!=', record.id)])
    #         if existing_type:
    #             raise exceptions.ValidationError("The property type name must be unique.")
    @api.depends('property_ids.offer_ids')
    def _compute_offer_count(self):
        for record in self:
            offer_count = 0
            for property in record.property_ids:
                offer_count += len(property.offer_ids)
            record.offer_count = offer_count            
