import functools

from dfe.util import merge_dicts_recursive


def _add_var(v):
    return {'vars': v}


def _add_if_not_present(func):
    @functools.wraps(func)
    def inner(attrs):
        result = func(attrs)
        merge_dicts_recursive(attrs, result)
    return inner


@_add_if_not_present
def auto_installer(attrs):
    base_img_name = attrs['vars']['base_img_name']
    if base_img_name == 'fedora':
        return _add_var({'installer': 'dnf'})
    elif base_img_name in ['rhel', 'centos']:
        return _add_var({'installer': 'yum'})
    return {}


@_add_if_not_present
def auto_dockerfile(attrs):
    return {'files': {'dockerfile': {'path': 'Dockerfile'}}}


AUTOATTRS = [auto_installer, auto_dockerfile]
