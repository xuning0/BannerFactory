class Error(Exception):
    pass


class IrregularError(Error):
    def __init__(self, message):
        self.message = message
