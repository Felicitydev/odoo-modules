from odoo import fields, models, api, _ 

class HospitalOperation(models.Model):
    _name = 'hospital.operation'
    _description = 'Opéraions Hopital'
    _rec_name = 'operation_name'
    _log_access = False # Remove fields create_date, create_uid, write_date write_uid
    
    doctor_id = fields.Many2one('res.users', string = "Docteur")
    operation_name = fields.Char(string="Nom")
    refernce_record = fields.Reference(selection=[('hospital.patient', 'Patients'),
                                                  ('hospital.appointment', 'Rendez-vous')] ,string="Record")
    
    @api.model 
    def name_create(self,name):
        return self.create({'operation_name' : name}).name_get()[0]