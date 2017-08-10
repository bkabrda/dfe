class DFEException(Exception):
    def __init__(self, cause):
        self.cause = cause

    def __str__(self):
        if isinstance(self.cause, str):
            return 'Error: {c}'.format(c=self.cause)
        return '{n}: {c}'.format(n=type(self.cause).__name__, c=str(self.cause))


class DFEParseException(DFEException):
    pass


class DFEConfigurationsVersionException(DFEException):
    def __init__(self, version):
        self.version = version

    def __str__(self):
        if self.version is None:
            return 'Error: configurations file provides no version'
        return 'Error: configuations file version "{v}" is not understood by this dfe version'.\
            format(v=self.version)
