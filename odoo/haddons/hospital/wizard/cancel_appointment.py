from odoo import api, fields, models
import datetime

class CancelAppointmentWizard(models.TransientModel):
    _name = 'cancel.appointment.wizard'
    _description = 'Cancel Appointment Wizard'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    @api.model 
    def default_get(self,fields):
        res =super(CancelAppointmentWizard,self).default_get(fields)
        res['date_cancel'] = datetime.date.today()
        return res
    
    appointment_id = fields.Many2one('hospital.appointment', string="Rendez-vous")
    reason = fields.Text(string="Raison de l'annulation")
    date_cancel = fields.Date(string="Date de l'annulation")
    
    def action_cancel(self):
        return 
    