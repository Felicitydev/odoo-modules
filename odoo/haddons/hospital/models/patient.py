from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import date
from dateutil import relativedelta


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hospital Patient'

    name = fields.Char(string="Nom", tracking=True)
    date_of_birth = fields.Date(string="Date de naissance")
    ref = fields.Char(string="Code", tracking=True)
    age = fields.Integer(string="Age", compute = '_compute_age', inverse='_inverse_compute_age', tracking=True, search = '_search_age')
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
    is_birthday = fields.Boolean(string="Anniversaire", compute='_compute_is_birthday')
    phone =fields.Char(string="Téléphone")
    email =fields.Char(string="Email")
    website =fields.Char(string="Website")
    
    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        for rec in self:
            if rec.date_of_birth and rec.date_of_birth > fields.Date.today():
                raise ValidationError(_("La date de naissance ne peut pas etre supérieure à la date du jour"))
            
    @api.ondelete(at_uninstall=False)
    def _check_appointment(self):
        for rec in self:
           if rec.appointment_ids:
                raise ValidationError(_("Vous ne pouvez pas supprimer un patient ayant un rendez-vous!"))
                
    
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
                
    @api.depends('age')
    def _inverse_compute_age(self):
       for rec in self:
            today = date.today()
            rec.date_of_birth = today - relativedelta.relativedelta(years=rec.age)
            
    def _search_age(self, operator, value):
        date_of_birth = date.today() - relativedelta.relativedelta(years=value)
        start_of_year = date_of_birth.replace(day=1, month=1)
        end_of_year = date_of_birth.replace(day=31, month=12)
        return [('date_of_birth', '>=', start_of_year), ('date_of_birth', '<=', end_of_year)]
    
    @api.depends('appointment_ids')            
    def compute_appointment_count(self):
        appointment_group = self.env['hospital.appointment'].read_group(domain=[('state', '=', 'done')], fields=['patient_id'], groupby=['patient_id'])
        for appointment in appointment_group:
            patient_id = appointment.get('patient_id')[0]
            if patient_id:
                patient_rec = self.browse(patient_id)
                patient_rec.appointment_count = appointment['patient_id_count']
                # S'il existe des patients n'ayant pas de rdv le système va renvoyer une erreur du style valueerror compute method failed to assign hospital.patient(id_patient,).appointment_count, pour cela on saisit les deux lignes suivantes | the system it's not able able to assign values for record 
                self -= patient_rec
        self.appointment_count = 0

    def action_test(self):
        return 
    
    @api.depends('date_of_birth')            
    def _compute_is_birthday(self):
        for rec in self:
            is_birthday = False
            if rec.date_of_birth:
                today = date.today()
                if today.day == rec.date_of_birth.day and today.month == rec.date_of_birth.month:
                    is_birthday = True
            rec.is_birthday = is_birthday