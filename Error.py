class Error(Exception):
    pass


class DrawLabelError(Error):
    def __init__(self, message):
        self.message = message
