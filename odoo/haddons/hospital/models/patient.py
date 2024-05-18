from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hospital Patient'

    name = fields.Char(string="Nom", tracking=True)
    ref = fields.Char(string="Code", tracking=True)
    age = fields.Integer(string="Age", tracking=True)
    gender = fields.Selection([('mal', 'Masculin'), ('female', 'Féminin')], string="Genre", tracking=True)
    active=fields.Boolean(string="Atif", default=True)