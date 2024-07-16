from odoo import api, fields, models, _

class PatientTag(models.Model):
    _name = 'patient.tag'
    _description = 'Patient Tag'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(string="Actif", default=True, copy=False)
    color = fields.Integer(string="Couleur")
    color2 = fields.Char(string="Couleur 2")
    sequence = fields.Integer(string="Sequence")
    
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('name'):
            default['name'] = self.name + " (copy)"
            # or we can use default['name'] = _("%s (copy)", self.name)
        default['sequence'] = 10
        return super(PatientTag, self).copy(default)
    
    _sql_constraints = [
        ('name_uniq', 'unique (name,active)', 'Le nom doit etre unique!'),
        ('check_sequence', 'check (sequence > 0)', 'La sequence doit etre un nombre positif!')
    ]