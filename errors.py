class ScanError(Exception):
    """
    Basic scan error.
    """
    pass


class InvalidData(ScanError):
    """
    Invalid data error. Is raised when an invalid query is sent to the API services
    """
    pass


class Forbidden(ScanError):
    """
    Forbidden access error. Is raised when an invalid key is sent to the API services
    """
    pass


class NotFound(ScanError):
    """
    Not found error. Is raised when a UPC code cannot be found by the API services
    """
    pass


class ExceedLimit(ScanError):
    """
    Daily limit error. Is raised when the API service's daily query limit is reached
    """
    pass


def raise_error(error):
    if error is InvalidData:
        msg = "INVALID UPC CODE!"
    elif error is Forbidden:
        msg = "INVALID API KEY!"
    elif error is NotFound:
        msg = "PRODUCT NOT FOUND!"
    elif error is ExceedLimit:
        msg = "API KEY DAILY LIMIT EXCEEDED!"
    else:
        msg = "-----SCAN FAILED!-----"
    raise error(msg)