import copy
import os

import yaml

from dfe.autoattrs import AUTOATTRS
from dfe.exceptions import (
    DFEParseException,
    DFEValidationException,
    DFEValueException
)
from dfe.util import merge_dicts_recursive


# TODO: I have a feeling that there has to be a simpler way to do this ... ;)
class ConfigurationsValidator(object):
    def __init__(self, raw_configs):
        self.raw_configs = raw_configs
        # in the future this will be useful for other validators,
        #   so that they know which version is being validated
        self.version = str(raw_configs.get('version', None))

    def validate(self):
        self.validate_version(self.raw_configs.get('version', None))
        self.validate_defaults(self.raw_configs.get('defaults', {}))
        self.validate_configurations(self.raw_configs.get('configurations', []))

    def validate_version(self, version):
        if version is None:
            raise DFEValidationException('version must be present')
        elif version not in [1, '1']:
            raise DFEValidationException(
                'version {v} is not understood by this dfe version'.format(v=version)
            )

    def validate_defaults(self, defaults):
        if not isinstance(defaults, dict):
            raise DFEValidationException('defaults must be a dict, is {t}'.
                                         format(t=type(defaults)))
        # this is actually just a normal config, except we don't enforce `name` to be here
        self.validate_config(defaults, name_required=False)

    def validate_configurations(self, configurations):
        if not isinstance(configurations, list):
            raise DFEValidationException('configurations must be a list, is {t}'.
                                         format(t=type(configurations)))
        for c in configurations:
            self.validate_config(c)

    def validate_config(self, config, name_required=True):
        if not isinstance(config, dict):
            raise DFEValidationException('configuration item must be a mapping, is {t}: {c}'.
                                         format(t=type(config), c=config))
        if name_required and 'name' not in config:
            raise DFEValidationException('name must be present in config entry {c}'.
                                         format(c=config))
        self.validate_name(config.get('name', ''))
        self.validate_tag(config.get('tag', ''))
        self.validate_files(config.get('files', {}))
        self.validate_vars(config.get('vars', {}))

    def validate_name(self, name):
        if not isinstance(name, str):
            raise DFEValidationException('name must be a string, is {t}: {n}'.
                                         format(t=type(name), n=name))

    def validate_tag(self, tag):
        if not isinstance(tag, str):
            raise DFEValidationException('tag must be a string, is {t}: {g}'.
                                         format(t=type(tag), g=tag))

    def validate_files(self, files):
        if not isinstance(files, dict):
            raise DFEValidationException('files must be a mapping, is {t}: {f}'.
                                         format(t=type(files), f=files))

        for name, attrs in files.items():
            self.validate_file(name, attrs)

    def validate_file(self, name, attrs):
        if not isinstance(name, str):
            raise DFEValidationException('file name must be a string, is {t}: {n}'.
                                         format(t=type(name), n=name))
        if 'path' not in attrs:
            raise DFEValidationException('"path" must be in file attributes of file {n}'.
                                         format(n=name))

    def validate_vars(self, vars):
        if not isinstance(vars, dict):
            raise DFEValidationException('vars must be a dict, is {t}: {v}'.
                                         format(t=type(vars), v=vars))
        for a in ['name', 'tag', 'files']:
            if a in vars:
                raise DFEValidationException(
                    '{a} must not be in vars, it is filled in automatically: {v}'.
                    format(a=a, v=vars)
                )
        for name, value in vars.items():
            if not isinstance(name, str):
                raise DFEValidationException('var name must be a string, is {t}: {n}'.
                                             format(t=type(name), n=name))


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
        try:
            with open(path) as f:
                c = yaml.load(f)
        except (yaml.scanner.ScannerError, IOError) as e:
            raise DFEParseException(e)

        ConfigurationsValidator(c).validate()

        version = c.get('version')
        defaults = c.get('defaults', {})
        configurations = c.get('configurations', {})

        return cls(version, defaults, configurations, output_path)


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
            if a not in ret:
                raise DFEValueException(attr, self.name)
            ret = ret[a]
        return ret

    @classmethod
    def from_raw_dict(cls, raw_config, defaults, output_path):
        # firstly, get a copy of defaults
        attrs = copy.deepcopy(defaults)
        # secondly, add values from raw_config (overwriting)
        merge_dicts_recursive(attrs, raw_config, overwrite=True)

        # make sure we have all the right attrs
        attrs.setdefault('name', '')
        attrs.setdefault('tag', '')
        attrs.setdefault('files', {})
        attrs.setdefault('vars', {})

        # thirdly, use AUTOATTRS (not overwriting)
        for func in AUTOATTRS:
            func(attrs)

        # expand output filenames
        for f, v in attrs['files'].items():
            v['outpath'] = os.path.join(
                output_path,
                '{orig}.{cname}'.format(orig=v['path'], cname=attrs['name'])
            )
        attrs['vars']['files'] = attrs['files']
        attrs['vars']['name'] = attrs['name']
        attrs['vars']['tag'] = attrs['tag']
        return cls(attrs)
