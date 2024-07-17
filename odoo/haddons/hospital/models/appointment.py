from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hospital Appointment'
    _rec_name = 'patient_id'

    patient_id = fields.Many2one(comodel_name='hospital.patient', string="Patients", ondelete='cascade') # if ondelete=cascade, delete the patient will delete all the appointment of the patient and if it's =restrict, we can't delete the appointment without deleting the patient
    gender = fields.Selection(related="patient_id.gender", readonly=False)
    appointment_time = fields.Datetime(string="Heure du rdv", default=fields.Datetime.now)
    booking_date = fields.Date(string="Heure de réservation", default=fields.Date.context_today)
    ref = fields.Char(string="Code", help="Identifiant unique de chaque patient", tracking=True)
    ref2 = fields.Char(string="Référence du rdv", help="Identifiant unique de chaque rdv", tracking=True)
    prescription = fields.Html(string="Prescription")
    active = fields.Boolean(string= "Active", default=True)
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High')], string="Priorité")
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('in_consultation', 'Consultation'),
        ('done', 'Fait'),
        ('cancel', 'Annulé')], default='draft', string="Statut", required=True)
    doctor_id = fields.Many2one('res.users', string = "Docteur", tracking=True)
    pharmacy_line_ids = fields.One2many('appointment.pharmacy.lines', 'appointment_id', string="Lignes de pharmacy")
    hide_sales_price = fields.Boolean(string="Masquer le pdv")

    @api.model
    def create(self,vals):
        vals['ref2'] = self.env['ir.sequence'].next_by_code('hospital.appointment')
        return super(HospitalAppointment,self).create(vals)
    
    def write(self,vals):
        if not self.ref and vals.get('ref'):
            vals['ref2'] = self.env['ir.sequence'].next_by_code('hospital.appointment')
        return super(HospitalAppointment,self).write(vals)
    
    def unlink(self):
        for rec in self:
            if rec.state != 'draft':
                raise ValidationError(_("Vous ne pouvez pas supprimer un rendez-vous à l'état est différent de brouilon."))
            return super(HospitalAppointment,self).unlink()
        

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        self.ref = self.patient_id.ref

    def action_test(self):
        return {
                'effect': {
                    'fadeout': 'slow', # L'image reste ficgée jusqu'à l'user effectue une action
                    'message': 'Click successfull',
                    'type': 'rainbow_man',
                }
            }

    def action_in_consultation(self):
        for rec in self:
            if rec.state == 'draft':
                rec.state ='in_consultation'
            
    def action_done(self):
        for rec in self:
            rec.state ='done'
            
    def action_cancel(self):
        action = self.env.ref('hospital.action_cancel_appointment').read()[0]
        return action
        # for rec in self:
        #     rec.state ='cancel'
            
    def action_draft(self):
        for rec in self:
            rec.state ='draft'