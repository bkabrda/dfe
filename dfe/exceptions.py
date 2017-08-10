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


class DFEConfigurationsVersionException(DFEException):
    def __init__(self, version):
        self.version = version

    def __str__(self):
        if self.version is None:
            return 'Error: configurations file provides no version'
        return 'Error: configuations file version "{v}" is not understood by this dfe version'.\
            format(v=self.version)


class DFETemplateNotFoundException(DFEException):
    def __init__(self, template, where):
        self.template = template
        self.where = where

    def __str__(self):
        return 'Error: template "{t}" not found in "{w}"'.format(t=self.template, w=self.where)
