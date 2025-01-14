from odoo import fields, models

class AccountWithholdingScale(models.Model):
    _name = 'account.withholding.scale'

    name = fields.Char(string='Nombre', required=True)
    company_id = fields.Many2one('res.company', string='Compañia')
    scale_lines = fields.One2many('account.withholding.scale.line', 'scale_id', string='Scale Lines')
    active = fields.Boolean(string='Activo', default=True)

    def obtain_withholding_scale(self, amount):
        for line in self.scale_lines:
            if line.to_amount <= amount and line.more_than_amount >= amount or line.to_amount == 0:
                return line.withholding_amount_base, line.incremental_percentage, line.excedent_fraction
        return 0, 0, 0
        
class AccountWithholdingScaleLine(models.Model):
    _name = 'account.withholding.scale.line'
    _order = 'sequence, id'

    scale_id = fields.Many2one('account.withholding.scale', string='Escala', required=True)
    more_than_amount = fields.Float(string='Importe: Mas de $')
    to_amount = fields.Float(string='Importe: A $')
    withholding_amount_base = fields.Float(string='Retendrán: $')
    incremental_percentage = fields.Float(string='Retendrán: Mas el %')
    excedent_fraction = fields.Float(string='Retendrán: S/Exc de %')
    sequence = fields.Integer(string='Secuencia')



