import copy

import yaml

AUTOADD_ATTRS = {
    lambda attrs: attrs['distro'] == 'fedora': {'installer': 'dnf'},
}


class Configurations(object):
    def __init__(self, version, defaults, raw_configs):
        self._version = version
        self._defaults = defaults
        self._raw_configs = raw_configs

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
        expanded = {}
        for n, attrs in self.raw_configs.items():
            # TODO: maybe create class for a single configuration
            expanded[n] = copy.deepcopy(self.defaults)
            expanded[n].update(attrs)
            # TODO: validate name is <name>-<version>, report error otherwise, if not
            #  defined in `attrs`
            if 'distro' not in attrs or 'distro_version' not in attrs:
                expanded[n]['distro'], expanded[n]['distro_version'] = n.split('-', 1)
        return expanded

    @property
    def configs_list(self):
        return self.expanded_configs.keys()

    def config_as_env_vars(self, config):
        res = []
        for k, v in self.expanded_configs[config].items():
            res.append('{k}={v}'.format(k=k.upper(), v=v))
        return ' '.join(res)

    @classmethod
    def from_file(cls, path):
        c = {}
        with open(path) as f:
            c = yaml.load(f)
        # TODO: report proper parsing errors
        return cls(c['version'], c['defaults'], c['configurations'])
