import logging
_logger = logging.getLogger(__name__)

def migrate(cr, installed_version):
    _logger.info("updating %s", installed_version)
    cr.execute("CREATE TABLE res_partner_payment_method AS SELECT id, name FROM payment_acquirer")
    return