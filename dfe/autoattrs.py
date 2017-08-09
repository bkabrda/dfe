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
def auto_dockerfile(attrs):
    return {'files': {'dockerfile': {'path': 'Dockerfile'}}}


@_add_if_not_present
def auto_tag(attrs):
    return {'tag': attrs['name']}


@_add_if_not_present
def auto_base_img_reg(attrs):
    return _add_var({'base_img_reg': ''})


def auto_base_img_reg_slash(attrs):
    # If we have non-empty registry without ending slash, we append it
    if attrs['vars']['base_img_reg'] and attrs['vars']['base_img_reg'][-1] != '/':
        attrs['vars']['base_img_reg'] += '/'


AUTOATTRS = [auto_dockerfile, auto_tag, auto_base_img_reg, auto_base_img_reg_slash]
