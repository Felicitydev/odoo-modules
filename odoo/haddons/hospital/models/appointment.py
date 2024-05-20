from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hospital Appointment'

    patient_id = fields.Many2one(comodel_name='hospital.patient', string="Patients")
    gender = fields.Selection(related="patient_id.gender", readonly=False)
    appointment_time = fields.Datetime(string="Heure du rdv", default=fields.Datetime.now)
    booking_date = fields.Date(string="Heure de réservation", default=fields.Date.context_today)