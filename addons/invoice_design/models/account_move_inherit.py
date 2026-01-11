from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = 'account.move'

    purchase_order_number = fields.Char(string='Purchase order Number')
