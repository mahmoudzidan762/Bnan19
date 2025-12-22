from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    x_customer_a_name = fields.Char(string='Customer Arabic Name')
    x_street_a_name = fields.Char(string='Street Arabic Name')
    x_district_a_name = fields.Char(string='District Arabic Name')
    x_city_a_name = fields.Char(string='City Arabic Name')
    x_country_a_name = fields.Char(string='Country Arabic Name')
