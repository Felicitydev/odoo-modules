# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    confirm_user_id = fields.Many2one('res.users', string="Confirmer l'utilisateur")

    def action_confirm(self):
        super(SaleOrder,self).action_confirm() #super(classname,args).function_name()
        self.confirm_user_id = self.env.user.id # Retrieve the current user