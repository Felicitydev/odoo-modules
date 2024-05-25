from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import date


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hospital Patient'

    name = fields.Char(string="Nom", tracking=True)
    date_of_birth = fields.Date(string="Date de naissance")
    ref = fields.Char(string="Code", tracking=True)
    age = fields.Integer(string="Age", compute = '_compute_age', tracking=True, store = True)
    gender = fields.Selection([('mal', 'Masculin'), ('female', 'Féminin')], string="Genre", tracking=True)
    active=fields.Boolean(string="Atif", default=True)

    @api.depends('date_of_birth')
    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year  
            else:
                rec.age = 0   