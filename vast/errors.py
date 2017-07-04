"""
All error from this project can be found here
"""

class IllegalModelStateError(Exception):
    """
    Raise when trying to create a Model which invalidates VAST specifications
    """
    pass


class ParseError(Exception):
    """
    Raise when encountering a parsing error
    """
    pass