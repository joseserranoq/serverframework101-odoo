from odoo import models, fields, exceptions

class estateProperty(models.Model):
    _name = 'estate.property'
    _inherit = 'estate.property'
#Invoice creation
    def action_sold(self): 
        res = super(estateProperty, self).action_sold()
        
        # Create invoice with two lines
        self.env['account.move'].create({
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [
                (0, 0, {
                    'name': 'Commission (6%)',
                    'quantity': 1,
                    'price_unit': self.selling_price * 0.06,
                }),
                (0, 0, {
                    'name': 'Administrative Fees',
                    'quantity': 1,
                    'price_unit': 100.0,
                }),
            ],
        })
        
        return res