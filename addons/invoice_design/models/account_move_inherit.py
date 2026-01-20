from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    purchase_order_number = fields.Char(string='Purchase order Number')
    totals_before_discount = fields.Monetary(
        string='Totals Before Discount',
        currency_field='currency_id',
        compute='_compute_totals_before_discount',
        store=True,
    )

    totals_after_discount = fields.Monetary(
        string='Totals After Discount',
        currency_field='currency_id',
        compute='_compute_totals_after_discount',
        store=True,
    )
    names = fields.Json(string='Names', compute='split_arabic')

    @api.depends('line_ids.total_price_after_discount')
    def _compute_totals_after_discount(self):
        for move in self:
            total = sum(line.total_price_after_discount for line in move.line_ids)
            move.totals_after_discount = total

    @api.depends('line_ids.total_price_without_tax_and_discount')
    def _compute_totals_before_discount(self):
        for move in self:
            total = sum(line.total_price_without_tax_and_discount for line in move.line_ids)
            move.totals_before_discount = total

    @api.depends('line_ids.product_id.name')
    def split_arabic(self):
        def is_arabic(char):
            return (
                    '\u0600' <= char <= '\u06FF' or
                    '\u0750' <= char <= '\u077F' or
                    '\u08A0' <= char <= '\u08FF' or
                    '\uFB50' <= char <= '\uFDFF' or
                    '\uFE70' <= char <= '\uFEFF'
            )

        for rec in self:
            result = []

            names = rec.line_ids.mapped('product_id.name')
            full_text = ' '.join(filter(None, names))

            current = ''
            current_lang = None

            for c in full_text:
                if c.strip() == '':
                    current += c
                    continue

                char_lang = 'ar' if is_arabic(c) else 'en'

                if current_lang is None:
                    current_lang = char_lang

                if char_lang != current_lang:
                    result.append(current.strip())
                    current = c
                    current_lang = char_lang
                else:
                    current += c

            if current.strip():
                result.append(current.strip())

            rec.names = [x for x in result if x]

            _logger.warning("SPLIT RESULT: %s", rec.names)


class AccountMoveLineInherit(models.Model):
    _inherit = 'account.move.line'

    total_price_without_tax_and_discount = fields.Monetary(
        string='Total Price without Tax and Discount',
        currency_field='currency_id',
        compute='_compute_total_price_without_tax_and_discount',
        store=True
    )

    total_price_after_discount = fields.Monetary(
        string='Total Price After Discount',
        currency_field='currency_id',
        compute='_compute_total_price_after_discount',
        store=True
    )

    @api.depends('quantity', 'price_unit')
    def _compute_total_price_without_tax_and_discount(self):
        for line in self:
            line.total_price_without_tax_and_discount = line.quantity * line.price_unit

    @api.depends('total_price_without_tax_and_discount', 'discount')
    def _compute_total_price_after_discount(self):
        for line in self:
            line.total_price_after_discount = line.total_price_without_tax_and_discount - (
                    (line.discount / 100) * line.total_price_without_tax_and_discount)
