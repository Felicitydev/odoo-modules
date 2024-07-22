from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AppointmentPharmacyLines(models.Model):
    _name = 'appointment.pharmacy.lines'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Appointment Pharmacy Lines'
    
    product_id = fields.Many2one('product.product', required=True)
    price = fields.Float(related='product_id.list_price')
    qty = fields.Integer(string="Quantité")
    appointment_id = fields.Many2one('hospital.appointment', string="Rdv")
    company_currency_id = fields.Many2one('res.currency', related='appointment_id.currency_id')
    price_subtotal = fields.Monetary(string="Total", compute='_compute_price_subtotal', currency_field='company_currency_id')
    
    @api.depends('price', 'qty')
    def _compute_price_subtotal(self):
        for rec in self:
            rec.price_subtotal = rec.price * rec.qty
    