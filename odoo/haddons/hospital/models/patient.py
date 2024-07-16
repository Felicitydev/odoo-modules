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
    appointment_id = fields.Many2one('hospital.appointment', string="Rdv")
    image = fields.Image(string="Image")
    tag_ids = fields.Many2many('patient.tag',string="Tags")
    appointment_count = fields.Integer(string="Nombre de rdv", compute='compute_appointment_count', store=True)
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string="Rendez-vous")
    parent = fields.Char(string="Parent")
    marital_status = fields.Selection([
        ('married' , 'Marié(e)'),
        ('single', 'Célibataire'), 
        ], string="Statut matrimonial", tracking=True)
    partner_name = fields.Char(string="Nom du partenaire")
    
    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        for rec in self:
            if rec.date_of_birth and rec.date_of_birth > fields.Date.today():
                raise ValidationError(_("La date de naissance ne peut pas etre supérieure à la date du jour"))
    
    @api.model
    def create(self,vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalPatient,self).create(vals)
    
    def write(self,vals):
        if not self.ref and vals.get('ref'):
            vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalPatient,self).write(vals)

    @api.depends('date_of_birth')
    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year  
            else:
                rec.age = 0   
    
    @api.depends('appointment_ids')            
    def compute_appointment_count(self):
        for rec in self:
            rec.appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])