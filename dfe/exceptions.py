class DFEException(Exception):
    def __init__(self, cause):
        self.cause = cause

    def __str__(self):
        if isinstance(self.cause, str):
            return 'Error: {c}'.format(c=self.cause)
        return '{n}: {c}'.format(n=type(self.cause).__name__, c=str(self.cause))


class DFEParseException(DFEException):
    pass


class DFEValueException(DFEException):
    def __init__(self, value, where):
        self.value = value
        self.where = where

    def __str__(self):
        return 'Error: value {v} not found in {w}'.format(v=self.value, w=self.where)


class DFEValidationException(DFEException):
    def __init__(self, err):
        self.err = err

    def __str__(self):
        return 'Configurations validation error: {e}'.format(e=self.err)


class DFETemplateNotFoundException(DFEException):
    def __init__(self, template, where):
        self.template = template
        self.where = where

    def __str__(self):
        return 'Error: template "{t}" not found in "{w}"'.format(t=self.template, w=self.where)
