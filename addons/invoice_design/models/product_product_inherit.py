from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ProductProduct(models.Model):
    _inherit = 'product.product'

    arabic_part = fields.Char(string='Arabic Part', compute='split_arabic', store=True)
    non_arabic_part = fields.Char(string='Non-Arabic Part', compute='split_arabic', store=True)

    @api.depends('name')
    def split_arabic(self):
        for rec in self:
            rec.arabic_part = ''.join(c for c in rec.name if '\u0600' <= c <= '\u06FF')
            rec.non_arabic_part = ''.join(c for c in rec.name if not ('\u0600' <= c <= '\u06FF'))
            return rec.arabic_part, rec.non_arabic_part
