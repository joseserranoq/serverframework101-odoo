from odoo import models, fields, exceptions

class estateProperty(models.Model):
    _name = 'estate.property'
    _inherit = 'estate.property'

    def action_sold(self): 
        res = super(estateProperty, self).action_sold()
        print('Response: ',res)
        return res