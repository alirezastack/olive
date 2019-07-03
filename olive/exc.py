

class GRPCError(Exception):
    def __init__(self, message, errors):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
        self.errors = errors


class CranberryServiceError(Exception):
    """Generic errors."""
    pass


class QuitException(Exception):
    pass


class ClientNotFound(Exception):
    pass


class AccessTokenNotFound(Exception):
    pass


class DuplicateClient(Exception):
    pass
