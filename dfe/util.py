import copy


def merge_dicts_recursive(d1, d2):
    """Update d1 with all keys of d2 that don't exist in d1, recursively."""
    for k, v in d2.items():
        if k in d1:
            if isinstance(v, dict) and k in d1:
                merge_dicts_recursive(d1[k], v)
            # else we don't want to overwrite d1[k]
        else:
            d1[k] = copy.deepcopy(v)
