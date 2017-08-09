import copy

import yaml

from dfe.autoattrs import AUTOATTRS
from dfe.util import merge_dicts_recursive


class Configurations(object):
    def __init__(self, version, defaults, raw_configs):
        self._version = version
        self._defaults = defaults
        self._raw_configs = raw_configs
        self._expanded_configs = None

    @property
    def version(self):
        return self._version

    @property
    def defaults(self):
        return self._defaults

    @property
    def raw_configs(self):
        return self._raw_configs

    @property
    def expanded_configs(self):
        if self._expanded_configs is None:
            self._expanded_configs = []
            for cfg in self.raw_configs:
                self._expanded_configs.append(Config.from_raw_dict(cfg, self._defaults))
        return self._expanded_configs

    @property
    def configs_names(self):
        return map(lambda c: c.name, self.expanded_configs)

    def get_expanded_config(self, config):
        return next(c for c in self.expanded_configs if c.name == config)

    @classmethod
    def from_file(cls, path):
        c = {}
        with open(path) as f:
            c = yaml.load(f)
        # TODO: report proper parsing errors
        return cls(c['version'], c['defaults'], c['configurations'])


class Config(object):
    def __init__(self, name, dockerfile, vars):
        self.name = name
        self.dockerfile = dockerfile
        self.vars = vars

    def as_env_vars(self):
        res = []
        for k, v in self.vars.items():
            res.append('{k}={v}'.format(k=k.upper(), v=v))
        return ' '.join(res)

    @classmethod
    def from_raw_dict(cls, raw_config, defaults):
        # firstly, get a copy of defaults
        attrs = copy.deepcopy(defaults)
        # secondly, override them by explicitly provided values from raw_config
        merge_dicts_recursive(attrs, raw_config)
        # thirdly, use AUTOATTRS
        for f in AUTOATTRS:
            f(attrs)
        return cls(attrs['name'], attrs['dockerfile'], attrs['vars'])
