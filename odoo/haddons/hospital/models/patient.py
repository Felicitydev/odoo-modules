from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Hospital Patient'

    name = fields.Char(string="Nom")
    ref = fields.Char(string="Code")
    age = fields.Integer(string="Age")
    gender = fields.Selection([('mal', 'Masculin'), ('female', 'Féminin')], string="Genre")
    active=fields.Boolean(string="Atif", default=True)