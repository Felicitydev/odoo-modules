from odoo import api, fields, models

class HospitalPatient(models.Model):
    _name = 'patient.tag'
    _description = 'Patient Tag'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(string="Actif", default=True)
    color = fields.Integer(string="Couleur")
    color2 = fields.Char(string="Couleur 2")