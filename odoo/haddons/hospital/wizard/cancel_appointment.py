from odoo import api, fields, models, _
import datetime
from odoo.exceptions import ValidationError
from datetime import date
from dateutil import relativedelta


class CancelAppointmentWizard(models.TransientModel):
    _name = 'cancel.appointment.wizard'
    _description = 'Cancel Appointment Wizard'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    @api.model 
    def default_get(self,fields):
        res =super(CancelAppointmentWizard,self).default_get(fields)
        res['date_cancel'] = datetime.date.today()
        if self.env.context.get('active_id'):
            res['appointment_id'] = self.env.context.get('active_id')
        return res
    
    appointment_id = fields.Many2one('hospital.appointment', string="Rendez-vous", domain=[('state', '=', 'draft'), ('priority', 'in',('0','1', False))])
    reason = fields.Text(string="Raison de l'annulation")
    date_cancel = fields.Date(string="Date de l'annulation")
    
    def action_cancel(self): 
        cancel_days = self.env['ir.config_parameter'].get_param('hospital.cancel_days')
        allowed_date = self.appointment_id.booking_date - relativedelta.relativedelta(day=int(cancel_days))
        if allowed_date <  date.today():
            raise ValidationError(_("Désolé, vous ne pouvez pas annuler un rendez-vous dont la date n'est pas encore arrivée."))
        self.appointment_id.state = 'cancel'
        return {
            'type' : 'ir.actions.client',
            'tag' : 'reload',
        }
    