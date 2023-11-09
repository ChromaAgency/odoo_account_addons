import logging
_logger = logging.getLogger(__name__)
def float_as_integer_without_separator(float_number, decimal_digits=2):
    """ Convert a float to an integer where the last two digits are the decimal part of the float but there is no separator
    We use str then int to avoid floating point math errors.
    """
    
    str_float = str(float_number)
    _logger.info(str_float)
    integers, decimals = str_float.split(".") if "." in str_float else (str_float, "")
    decimals = decimals[:decimal_digits]
    if len(decimals) < decimal_digits:
        decimals = decimals + ("0" * (decimal_digits - len(decimals)))
    return int("".join([integers, decimals]))