# Return 422 Unprocessable Content
class UnprocessableContentError(Exception):
    pass


class InvalidMediaTypeError(UnprocessableContentError):
    pass


class UnknownMediaTypeError(UnprocessableContentError):
    pass


class UnsupportedMediaTypeError(UnprocessableContentError):
    pass