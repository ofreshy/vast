"""

"""
from itertools import chain

from vast.errors import IllegalModelStateError


def make_required_checker(required):
    """
    Closure over set of required of attributes, e.g.

    required = ("id", "name")

    :param required: iterable of attribute names
    :return: check function which takes in dictionary of kw args
    """
    msg = "Missing required attribute :'{attr_name}'"
    required = required or []

    def check(args_dict):
        errors = [
            msg.format(attr_name=attr_name)
            for attr_name in required
            if attr_name not in args_dict
        ]
        return errors

    return check


def make_converter(converters, required):
    """
    Convert fields in args dict

    :param converters: iterable of tuples where each tuple
    first element is callable type (such as int / float etc.) and
    second element is an iterable of attribute names to be converted to that type
    :param required: set of required attributes
    :return: check function which takes in dictionary of kw args
    """
    converters = converters or []
    msg = "Cannot convert '{attr_name}={value}' to '{type}'"

    def convert(args_dict):
        errors = []

        for _type, attr_names in converters:
            for attr_name in attr_names:
                if attr_name not in args_dict:
                    continue
                v = args_dict.get(attr_name)
                if v is None:
                    if attr_name in required:
                        errors.append(
                            msg.format(
                                attr_name=attr_name,
                                value=v,
                                type=_type,
                            )
                        )
                    continue

                try:
                    if _type != bool:
                        value = _type(v)
                    else:
                        value = to_bool(v)
                    args_dict[attr_name] = value
                except (TypeError, ValueError):
                    # enum conversion errors are value errors
                    errors.append(
                        msg.format(
                            attr_name=attr_name,
                            value=v,
                            type=_type,
                        )
                    )
        return errors
    return convert


def make_some_of_checker(some_ofs):
    """
    Takes in a list of tuples [t1, t2, .., tn]
    Where each tuple has a tuple of attributes as first element and an int as second ((a1, a2, .. , an), up_to)
    Where the up_to specifies how many of the attributes can co-exist
    In this sense, a one-of is where up_to is 1

    e.g.
    say that t1 is (("att1", "att2"), 1) that means that only att1 or att2 can be present, but not both
    :param some_ofs: list of tuples. See above for format
    :return: check function which takes in dictionary of kw args
    """
    msg = "Only {up_to} attribute from {attr_names} should be found, but found {existing}"

    def checker(args_dict):
        errors = []
        for (attr_names, up_to) in some_ofs:
            existing = [attr_name for attr_name in attr_names if args_dict.get(attr_name)]
            if len(existing) > up_to:
                errors.append(
                    msg.format(
                        up_to=up_to,
                        attr_names=attr_names,
                        existing=existing,
                    )
                )
        return errors

    return checker


def make_class_checker(classes, required):
    """

    :param classes: iterable of tuples where
     first element is the class itself
     second element is the attr name that should be instance of that class
     third element is a bool where if true indicates the attr_name is a container
    :param required: set of required fields
    :return: check function which takes in dictionary of kw args
    """
    classes = classes or []
    msg = "Attribute {attr_name} is not of class {class_name} but of type {type}"

    def check(args_dict):
        errors = []

        def check_for_class(v, clazz):
            if not isinstance(v, clazz):
                errors.append(
                    msg.format(
                        attr_name=attr_name,
                        class_name=clazz,
                        type=type(value),
                    )
                )

        for attr_name, clazz, container_type in classes:
            if attr_name not in args_dict:
                continue
            value = args_dict.get(attr_name)
            if value is None:
                if attr_name in required:
                    # This will add an error
                    check_for_class(value, clazz)
                continue

            if not container_type:
                check_for_class(value, clazz)
            else:
                for v in value:
                    check_for_class(v, clazz)

        return errors

    return check


def to_bool(value):
    value = str(value).lower()
    if value in ("none", "0", "false"):
        return False
    if value in ("true", "1"):
        return True
    raise ValueError


def with_checker_converter():
    """Add a checker converter method to class
    """

    def _add_checker_converter(cls):
        required = frozenset(getattr(cls, "REQUIRED", []))
        ccs = (
            make_required_checker(required),
            make_some_of_checker(getattr(cls, "SOME_OFS", [])),
            make_converter(getattr(cls, "CONVERTERS", []), required),
            make_class_checker(getattr(cls, "CLASSES", []), required),
        )

        def _check_and_convert(args_dict):
            # we are going to mutate args when we convert into types
            args = args_dict.copy()
            errors = list(
                chain.from_iterable(
                    (cc(args) for cc in ccs)
                )
            )
            if errors:
                msg = "cannot instantiate class : {name}. Got Errors : {errors}"
                raise IllegalModelStateError(msg.format(name=cls.__name__, errors=errors))

            return cls(**args)

        # Set the check and convert method.
        # Make cc a static method so it can be called on the class level
        setattr(cls, "check_and_convert", staticmethod(_check_and_convert))

        return cls
    return _add_checker_converter
