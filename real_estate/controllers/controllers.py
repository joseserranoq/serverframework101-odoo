from odoo import http
from odoo.http import request
import json


class RealEstate(http.Controller):
#     @http.route('/real_estate/real_estate', auth='public')
#     def index(self, **kw):
#         return "Hello, world"
    @http.route('/real_estate/api/properties', type='http', auth='public', methods=['GET'])
    def api_properties(self, **params):
        """
        Returns a list of estate.property records as JSON.
        Optional query params:
          - fields: comma-separated list of fields (e.g. id,name,expected_price)
          - limit: integer limit (default 50)
          - offset: integer offset (default 0)
          - order: order string (e.g. id desc)
        """
        env = http.request.env
        # Parse query parameters
        fields = params.get('fields')
        fields = [f.strip() for f in fields.split(',')] if fields else None
        try:
            limit = int(params.get('limit', 50))
        except Exception:
            limit = 50
        try:
            offset = int(params.get('offset', 0))
        except Exception:
            offset = 0
        order = params.get('order')

        try:
            records = env['estate.property'].sudo().search_read(
                domain=[], fields=fields, offset=offset, limit=limit, order=order
            )
            return http.request.make_json_response({
                'count': len(records),
                'results': records,
            })
        except Exception as e:
            return http.request.make_json_response({
                'error': 'Bad Request',
                'details': str(e),
            }, status=400)

    @http.route('/real_estate/api/properties/<int:prop_id>', type='http', auth='public', methods=['GET'])
    def api_property_detail(self, prop_id, **params):
        """
        Returns a single estate.property record by ID as JSON.
        Optional query param:
          - fields: comma-separated list of fields
        """
        env = http.request.env
        fields = params.get('fields')
        fields = [f.strip() for f in fields.split(',')] if fields else None

        rec = env['estate.property'].sudo().browse(prop_id)
        if not rec.exists():
            return http.request.make_json_response({'error': 'Not Found'}, status=404)

        try:
            data = rec.read(fields=fields)[0] if fields or True else rec.read()[0]
            return http.request.make_json_response(data)
        except Exception as e:
            return http.request.make_json_response({
                'error': 'Bad Request',
                'details': str(e),
            }, status=400)

#     @http.route('/real_estate/real_estate/objects/<model("real_estate.real_estate"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('real_estate.object', {
#             'object': obj
#         })

