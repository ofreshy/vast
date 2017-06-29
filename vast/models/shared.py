"""

"""
from itertools import chain

import attr

from vast.errors import IllegalModelStateError


@attr.s()
class SomeOf(object):
    """
    Defines a some of constraint on some attributes in a class

    """
    attr_names = attr.ib()
    at_least = attr.ib(default=1)
    up_to = attr.ib(default=1)

    def check(self, args_dict):
        # do not use 'in args_dict' since a key with a None value is not considered as exists
        existing = [attr_name for attr_name in self.attr_names if args_dict.get(attr_name) is not None]
        if len(existing) > self.up_to:
            msg = "Only {up_to} attribute from {attr_names} should be found, but found {existing}"
            return msg.format(
                up_to=self.up_to,
                attr_names=self.attr_names,
                existing=existing
            )
        if len(existing) < self.at_least:
            msg = "At least {at_least} attributes from {attr_names} should be found, but found {existing}"
            return msg.format(
                at_least=self.at_least,
                attr_names=self.attr_names,
                existing=existing
            )
        return None


@attr.s()
class Converter(object):
    attr_names = attr.ib()
    type = attr.ib()

    def _error(self, attr_name, value):
        msg = "Cannot convert '{attr_name}={value}' to '{type}'"
        return msg.format(
                attr_name=attr_name,
                value=value,
                type=self.type,
            )

    def _convert(self, value):
        return self.type(value)

    def execute(self, args_dict, required):
        errors = []
        for attr_name in self.attr_names:
            if attr_name not in args_dict:
                continue

            v = args_dict.get(attr_name)
            if v is None:
                if attr_name in required:
                    errors.append(self._error(attr_name, v))
                continue

            try:
                args_dict[attr_name] = self._convert(v)
            except (TypeError, ValueError):
                # enum conversion errors are value errors
                errors.append(self._error(attr_name, v))
        return errors



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
    e.g.
    converters = [(int, ("num_of_goal", "people"), ("float", "goal_per_person_ratio", )]

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

        def add_error():
            errors.append(
                msg.format(
                    attr_name=attr_name,
                    value=v,
                    type=_type,
                )
            )

        def _convert(value):
            return to_bool(value) if _type == bool else _type(value)

        for _type, attr_names in converters:
            for attr_name in attr_names:

                if attr_name not in args_dict:
                    continue

                v = args_dict.get(attr_name)
                if v is None:
                    if attr_name in required:
                        add_error()
                    continue

                try:
                    args_dict[attr_name] = _convert(v)
                except (TypeError, ValueError):
                    # enum conversion errors are value errors
                    add_error()
        return errors
    return convert


def make_converter_2(converters, required):
    """
    Convert fields in args dict
    e.g.
    converters = [(int, ("num_of_goal", "people"), ("float", "goal_per_person_ratio", )]

    :param converters: iterable of tuples where each tuple
    first element is callable type (such as int / float etc.) and
    second element is an iterable of attribute names to be converted to that type
    :param required: set of required attributes
    :return: check function which takes in dictionary of kw args
    """
    def convert(args_dict):
        errors = list(
            chain.from_iterable(
                c.execute(args_dict, required) for c in converters
            )
        )
        return errors
    return convert


def make_some_of_checker(some_ofs):
    """
    Checks for SomeOf constraints between attributes

    :param some_ofs: list of SomeOf instances
    :return: check function which takes in dictionary of kw args
    """
    def checker(args_dict):
        errors = (
            some_of.check(args_dict) for some_of in some_ofs
        )
        return  [e for e in errors if e]

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
            make_converter_2(getattr(cls, "CONVERTERS_2", []), required),
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
