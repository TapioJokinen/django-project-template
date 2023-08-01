import re
from decimal import Decimal


def to_camel_case(snake_str):
    """Converts snake-case to camel-case."""
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


def obj_to_camel_case(obj):
    """Converts dict keys from snake-case to camel-case."""
    if isinstance(obj, list):
        return [obj_to_camel_case(i) for i in obj]

    if not isinstance(obj, dict):
        return obj

    new_dict = {}

    for k, v in obj.items():
        if isinstance(v, (dict)):
            new_dict[to_camel_case(k)] = obj_to_camel_case(v)
        elif isinstance(v, list):
            new_dict[to_camel_case(k)] = [obj_to_camel_case(i) for i in v]
        else:
            new_dict[to_camel_case(k)] = v if isinstance(v, (int, float, Decimal)) else str(v)
    return new_dict


def to_snake_case(name):
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    name = re.sub("__([A-Z])", r"_\1", name)
    name = re.sub("([a-z0-9])([A-Z])", r"\1_\2", name)
    return name.lower()
