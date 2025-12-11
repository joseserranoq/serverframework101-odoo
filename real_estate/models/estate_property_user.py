from odoo import models, fields

class EstatePropertyUser(models.Model):
    _name = 'res.users'
    _inherit = 'res.users'

    # Only show properties that are not sold or canceled
    property_ids = fields.One2many(
        'estate.property',
        'user_id',
        string='Properties',
        domain=[('state', 'not in', ['sold', 'canceled'])],
        help='List of available properties managed by this user.',
    )