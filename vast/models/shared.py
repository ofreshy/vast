"""

"""
from functools import wraps


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


def make_one_of_checker(one_ofs):
    one_ofs = one_ofs or []
    msg = "Only 1 attribute from {attr_names} should be found, but found {existing}"

    def checker(args_dict):
        found = {}
        errors = []
        for attr_names in one_ofs:
            existing = [attr_name for attr_name in attr_names if args_dict.get(attr_name)]
            if len(existing) != 1:
                errors.append(
                    msg.format(
                        attr_names=attr_names,
                        existing=existing,
                    )
                )
            else:
                attr_name = existing[0]
                found[attr_name] = args_dict[attr_name]
        return found, errors

    return checker


def make_converter(converters, required):
    converters = converters or []
    msg = "Cannot convert '{attr_name}={value}' to '{type}'"

    def convert(args_dict):
        converted = {}
        errors = []

        for attr_name, c in converters:
            if attr_name not in args_dict:
                continue
            v = args_dict.get(attr_name)
            if v is None:
                if attr_name in required:
                    errors.append(
                        msg.format(
                            attr_name=attr_name,
                            value=v,
                            type=c,
                        )
                    )
                continue

            try:
                converted[attr_name] = c(v)
            except TypeError:
                errors.append(
                    msg.format(
                        attr_name=attr_name,
                        value=v,
                        type=c,
                    )
                )
        return converted, errors
    return convert


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
                    check_for_class(value, clazz)
                continue

            found[attr_name] = value

            if not container_type:
                check_for_class(value, clazz)
            else:
                for v in value:
                    check_for_class(v, clazz)

        return found, errors

    return check


def make_enum_checker(enums, required):
    enums = enums or ()
    msg = "'{value}' for {attr_name} cannot be assigned enum value from {enum}"

    def check(args_dict):
        found = {}
        errors = []
        for attr_name, enum in enums:
            if attr_name not in args_dict:
                continue

            value = args_dict.get(attr_name)
            if value is None:
                if attr_name in required:
                    errors.append(
                        msg.format(
                            value=value,
                            attr_name=attr_name,
                            enum=enum,
                        )
                    )
                continue

            try:
                vnum = enum.from_string(str(value))
                # TODO should throw here a value error
                if vnum is None:
                    raise ValueError
                found[attr_name] = vnum
            except ValueError:
                errors.append(
                    msg.format(
                        value=value,
                        attr_name=attr_name,
                        enum=enum,
                    )
                )
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


def pre_make(
        required=None,
        one_ofs=None,
        convertors=None,
        enums=None,
        classes=None,
        bools=None,
):
    required = required or set(required)
    ccs = (
        make_required_checker(required),
        make_one_of_checker(one_ofs),
        make_converter(convertors, required),
        make_enum_checker(enums, required),
        make_bool_converter(bools, required),
        make_class_checker(classes, required)
    )

    def wrapper(make_func):
        @wraps(make_func)
        def new_make(**kwargs):
            found = {}
            errors = []

            for cc in ccs:
                f, e = cc(kwargs)
                found.update(f), errors.extend(e)

            if errors:
                #TODO
                raise ValueError(errors)

            return make_func(**found)

        return new_make
    return wrapper
