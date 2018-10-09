class NotFoundError(Exception):
    """
    Custom error raised when specified entities are not found.
    """
    pass


class InvalidSource(Exception):
    """
    Custom error raised when the energy source is not a valid type.
    """
    pass
