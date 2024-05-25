from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hospital Appointment'
    _rec_name = 'patient_id'

    patient_id = fields.Many2one(comodel_name='hospital.patient', string="Patients")
    gender = fields.Selection(related="patient_id.gender", readonly=False)
    appointment_time = fields.Datetime(string="Heure du rdv", default=fields.Datetime.now)
    booking_date = fields.Date(string="Heure de réservation", default=fields.Date.context_today)
    ref = fields.Char(string="Code", tracking=True)
    prescription = fields.Html(string="Prescription")
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High')], string="Priorité")
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('in_consultation', 'Consultation'),
        ('done', 'Fait'),
        ('cancel', 'Fermé')], default='draft', string="Statut", required=True)


    @api.onchange('patient_id')
    def onchange_patient_id(self):
        self.ref = self.patient_id.ref

    def action_test(self):
        print("....................................................................................................")