from odoo import fields, models

class AccountWithholdingScale(models.Model):
    _name = 'account.withholding.group'

    name = fields.Char(string='Nombre', required=True)
    company_id = fields.Many2one('res.company', string='Compañia')
    group_lines = fields.One2many('account.withholding.group.line', 'group_id', string='Lineas de grupo')
    active = fields.Boolean(string='Activo', default=True)

    def obtain_withholding_group_amount(self, partner):
        for line in self.group_lines:
            if line.group_ref == partner.withholding_group:
                return line.group_amount
        return 0

class AccountWithholdingGroupLine(models.Model):
    _name = 'account.withholding.group.line'
    _order = 'sequence, id'

    group_id = fields.Many2one('account.withholding.group', string='Grupo', required=True)
    group_ref = fields.Char(string='Referencia', required=True)
    group_amount = fields.Float(string='Monto')
    sequence = fields.Integer(string='Secuencia')


