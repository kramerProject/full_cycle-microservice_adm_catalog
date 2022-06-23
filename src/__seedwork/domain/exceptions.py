class InvalidUuidException(Exception):
    def __init__(self, error = "ID must be a valid uuid") -> None:
        super().__init__(error)


class ValidationException(Exception):
    pass