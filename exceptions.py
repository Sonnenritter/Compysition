

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class OutofBoundsError(Error):
    pass

class InputError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expr -- input expression in which the error occurred
        msg  -- explanation of the error
    """

    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = msg


class FullBarError(Error):
    def __init__(self, msg):
        self.msg = msg