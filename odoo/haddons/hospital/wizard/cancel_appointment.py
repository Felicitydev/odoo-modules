from odoo import api, fields, models

class CancelAppointmentWizard(models.TransientModel):
    _name = 'cancel.appointment.wizard'
    _description = 'Cancel Appointment Wizard'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    appointment_id = fields.Many2one('hospital.appointment', string="Rendez-vous")
    
    def action_cancel(self):
        return 