from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval

DEFAULT_ENV_VARIABLES = """
# Add any default code or environment variables you want here
# For example:
# model_name = 'odoo.playground'
"""

class OdooPlayGround(models.Model):
    _name = "odoo.playground"
    _description = "Odoo PlayGround" 
    
    model_id = fields.Many2one('ir.model', string="Modeèle")
    code = fields.Text(string="Code", default=DEFAULT_ENV_VARIABLES)
    result = fields.Text(string="Résultat")

    def action_execute(self):
        try:
            if self.model_id:
                model = self.env[self.model_id.model]
            else:
                model = self
            self.result = safe_eval(self.code.strip(), {'self' : model})
        except Exception as e:
            self.result = str(e)