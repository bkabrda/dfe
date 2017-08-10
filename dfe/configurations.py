import copy
import os

import yaml

from dfe.autoattrs import AUTOATTRS
from dfe.util import merge_dicts_recursive


class Configurations(object):
    def __init__(self, version, defaults, raw_configs, output_path):
        self._version = version
        self._defaults = defaults
        self._raw_configs = raw_configs
        self._output_path = output_path
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
                self._expanded_configs.append(
                    Config.from_raw_dict(cfg, self._defaults, self._output_path)
                )
        return self._expanded_configs

    @property
    def configs_names(self):
        return map(lambda c: c.name, self.expanded_configs)

    def get_expanded_config(self, config):
        return next(c for c in self.expanded_configs if c.name == config)

    @classmethod
    def from_file(cls, path, output_path):
        # we need to know output_path, so that we can use it in expanded configs
        c = {}
        with open(path) as f:
            c = yaml.load(f)
        # TODO: report proper parsing errors
        return cls(c['version'], c['defaults'], c['configurations'], output_path)


class Config(object):
    def __init__(self, attrs):
        self.attrs = attrs

    @property
    def name(self):
        return self.attrs['name']

    @property
    def files(self):
        return self.attrs['files']

    @property
    def tag(self):
        return self.attrs['tag']

    @property
    def vars(self):
        return self.attrs['vars']

    def get_value(self, attr):
        if attr == '.':
            return self.attrs
        alist = attr.split('.')
        ret = self.attrs
        for a in alist:
            ret = ret[a]
        return ret

    @classmethod
    def from_raw_dict(cls, raw_config, defaults, output_path):
        # firstly, get a copy of defaults
        attrs = copy.deepcopy(defaults)
        # secondly, add values from raw_config (overwriting)
        merge_dicts_recursive(attrs, raw_config, overwrite=True)
        attrs.setdefault('files', {})
        # thirdly, use AUTOATTRS (not overwriting)
        for func in AUTOATTRS:
            func(attrs)

        # expand output filenames
        for f, v in attrs['files'].items():
            v['outpath'] = os.path.join(
                output_path,
                '{orig}.{cname}'.format(orig=v['path'], cname=attrs['name'])
            )
        # TODO: make "name", "tag" "files" a prohibited name in "vars" because of this
        attrs['vars']['files'] = attrs['files']
        attrs['vars']['name'] = attrs['name']
        attrs['vars']['tag'] = attrs['tag']
        return cls(attrs)
