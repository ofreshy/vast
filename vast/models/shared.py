"""

"""
from vast.errors import IllegalModelStateError



def make_required_checker(required):
    msg = "Missing required attribute :'{attr_name}'"
    required = required or []

    def check(args_dict):
        found = {}
        errors = []
        for attr_name in required:
            # check with in as None can be a valid value for some required fields!
            if attr_name in args_dict:
                found[attr_name] = args_dict[attr_name]
            else:
                errors.append(
                    msg.format(
                        attr_name=attr_name,
                    )
                )
        return found, errors
    return check


def make_converter(converters, required):
    converters = converters or []
    msg = "Cannot convert '{attr_name}={value}' to '{type}'"

    def convert(args_dict):
        converted = {}
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
                    converted[attr_name] = value
                except (TypeError, ValueError):
                    # enum conversion errors are value errors
                    errors.append(
                        msg.format(
                            attr_name=attr_name,
                            value=v,
                            type=_type,
                        )
                    )
        return converted, errors
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
    :return: some_of_checker_function
    """
    msg = "Only {up_to} attribute from {attr_names} should be found, but found {existing}"

    def checker(args_dict):
        found = {}
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
            else:
                found.update(
                    {attr_name:args_dict.get(attr_name) for attr_name in attr_names}
                )
        return found, errors

    return checker


def make_class_checker(classes, required):
    classes = classes or []
    msg = "Attribute {attr_name} is not of class {class_name} but of type {type}"

    def check(args_dict):
        found = {}
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
                else:
                    found[attr_name] = value
                continue

            if not container_type:
                check_for_class(value, clazz)
            else:
                for v in value:
                    check_for_class(v, clazz)

        return found, errors

    return check



def make_bool_converter(bools, required):
    bools = bools or []
    msg = "Cannot convert '{attr_name}={attr_value}' to boolean"

    def convert(args_dict):
        found = {}
        errors = []
        for attr_name in bools:
            if attr_name not in args_dict:
                continue
            attr_value = args_dict[attr_name]
            if attr_value is None:
                if attr_name in required:
                    errors.append()
                continue

            try:
                found[attr_name] = to_bool(attr_value)
            except ValueError:
                errors.append(
                    msg.format(
                        attr_name=attr_name,
                        attr_value=attr_value,
                    )
                )

        return found, errors

    return convert


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
            make_bool_converter(getattr(cls, "BOOLS", []), required),
            make_class_checker(getattr(cls, "CLASSES", []), required),
        )

        def _check_and_convert(args_dict):
            args = args_dict.copy()
            errors = []
            for cc in ccs:
                f, e = cc(args_dict)
                args.update(f), errors.extend(e)

            if errors:
                msg = "cannot instantiate class : {name}. Got Errors : {errors}"
                raise IllegalModelStateError(msg.format(name=cls.__name__, errors=errors))

            return cls(**args)

        # Set the check and convert method.
        # Make cc a static method so it can be called on the class level
        setattr(cls, "check_and_convert", staticmethod(_check_and_convert))

        return cls
    return _add_checker_converter
