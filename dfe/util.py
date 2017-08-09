import copy


def merge_dicts_recursive(d1, d2, overwrite=False):
    """Update d1 with all keys of d2, recursively.

    If `overwrite` is `False`, only keys not existing in d1 are added;
    otherwise existing keys are overwritten.
    """
    for k, v in d2.items():
        if k in d1:
            if isinstance(v, dict):
                merge_dicts_recursive(d1[k], v, overwrite)
            elif overwrite:
                d1[k] = copy.deepcopy(v)
        else:
            d1[k] = copy.deepcopy(v)
