import logging
_logger = logging.getLogger(__name__)

def migrate(cr, installed_version):
    _logger.info("updating 0.0.0 %s", installed_version)
    cr.execute("CREATE TABLE IF NOT EXISTS res_partner_payment_method (id SERIAL PRIMARY KEY, name VARCHAR)")
    cr.execute("INSERT INTO res_partner_payment_method SELECT id, name FROM payment_acquirer")
    cr.execute("CREATE TABLE IF NOT EXISTS account_payment_condition_res_partner_payment_method_rel (account_payment_condition_id INTEGER references account_payment_condition(id) , res_partner_payment_method_id INTEGER references res_partner_payment_method(id))")
    cr.execute("INSERT INTO account_payment_condition_res_partner_payment_method_rel SELECT account_payment_condition_id, payment_acquirer_id AS res_partner_payment_method_id FROM account_payment_condition_payment_acquirer_rel")
    return