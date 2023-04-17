import logging
_logger = logging.getLogger(__name__)

def migrate(cr, installed_version):
    _logger.info("updating 0.0.0 %s", installed_version)
    cr.execute("CREATE TABLE res_partner_payment_method AS SELECT id, name FROM payment_acquirer")
    cr.execute("CREATE TABLE account_payment_condition_res_partner_payment_method_rel AS SELECT account_payment_condition_id, payment_acquirer_id AS res_partner_payment_method_id FROM payment_acquirer")
    return