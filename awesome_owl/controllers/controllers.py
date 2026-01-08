from odoo import http
from odoo.http import request, route

class OwlPlayground(http.Controller):
    @http.route(['/awesome_owl'], type='http', auth='public')
    def show_playground(self):
        """
        Renders the owl playground page
        """
        return request.render('awesome_owl.playground')

    @http.route(['/awesome_owl/data'], type='http', auth='public', methods=['GET'])
    def get_data(self, **kwargs):
        """
        Provides sample data for the owl playground as JSON (HTTP)
        """
        sample_data = {
            'message': 'Hello from Odoo!',
            'items': [
                {'id': 1, 'name': 'Item 1'},
                {'id': 2, 'name': 'Item 2'},
                {'id': 3, 'name': 'Item 3'},
            ],
        }

        return request.make_json_response(sample_data)