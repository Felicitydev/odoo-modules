# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    confirm_user_id = fields.Many2one('res.users', string="Confirmer l'utilisateur")
