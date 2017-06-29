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
        errors = []
        # do not use 'in args_dict' since a key with a None value is not considered as exists
        existing = [
            attr_name for attr_name in self.attr_names
            if args_dict.get(attr_name) is not None
        ]
        if len(existing) > self.up_to:
            msg = "Only {up_to} attribute from {attr_names} should be found, but found {existing}"
            errors.append(
                msg.format(
                    up_to=self.up_to,
                    attr_names=self.attr_names,
                    existing=existing
                )
            )
        elif len(existing) < self.at_least:
            msg = "At least {at_least} attributes from {attr_names} should be found, but found {existing}"
            errors.append(
                msg.format(
                    at_least=self.at_least,
                    attr_names=self.attr_names,
                    existing=existing
                )
            )
        return errors


@attr.s()
class Converter(object):
    """
    Convert a value to given type
    """
    type = attr.ib()
    attr_names = attr.ib()

    def __attrs_post_init__(self):
        if self.type == bool:
            self._convert = to_bool
        else:
            self._convert = self.type

    def _add_error(self, errors, attr_name, value):
        msg = "Cannot convert '{attr_name}={value}' to '{type}'"
        errors.append(
            msg.format(
                attr_name=attr_name,
                value=value,
                type=self.type,
            )

        )

    def convert(self, args_dict, required):
        errors = []
        for attr_name in self.attr_names:
            v = args_dict.get(attr_name)
            if v is None:
                if attr_name in required:
                    self._add_error(errors, attr_name, v)
                continue

            try:
                args_dict[attr_name] = self._convert(v)
            except (TypeError, ValueError):
                # enum conversion errors are value errors
                self._add_error(errors, attr_name, v)
        return errors


@attr.s()
class ClassChecker(object):
    """
    Checks that a value is an instance of a class
    """
    attr_name = attr.ib()
    clazz = attr.ib()
    is_container = attr.ib(default=False)

    def _add_error(self, errors, v):
        msg = "Attribute {attr_name} is not of class {class_name} but of type {type}"
        errors.append(
            msg.format(
                attr_name=self.attr_name,
                class_name=self.clazz.__name__,
                type=type(v),
            )
        )

    def _check(self, errors, v):
        if self.is_container:
            vs = (_v for _v in v)
        else:
            vs = (v, )

        for value in vs:
            if not isinstance(value, self.clazz):
                self._add_error(errors, value)

    def check(self, args_dict, required):
        errors = []
        value = args_dict.get(self.attr_name)
        if value is None:
            if self.attr_name in required:
                self._add_error(errors, value)
        else:
            self._check(errors, value)

        return errors


def _check_required(args_dict, required):
    """

    :param args_dict: dict of att_names to att_values
    :param required: iterable of attribute names
    :return: list of errors if any found or empty list otherwise
    """
    msg = "Missing required attribute :'{attr_name}'"
    return [
        msg.format(attr_name=attr_name)
        for attr_name in required
        if attr_name not in args_dict
    ]


def _check_conversions(args_dict, required, converters):
    """

    :param args_dict: dict of att_names to att_values
    :param required: iterable of attribute names
    :param converters: iterable of Converter instances
    :return: list of errors if any found or empty list otherwise
    """
    return list(
        chain.from_iterable(
            c.convert(args_dict, required) for c in converters
        )
    )


def _check_some_ofs(args_dict, some_ofs):
    """

    :param args_dict: dict of att_names to att_values
    :param some_ofs: iterable of SomeOf instances
    :return: list of errors if any found or empty list otherwise
    """
    return list(
        chain.from_iterable(
            s.check(args_dict) for s in some_ofs
        )
    )


def _check_classes(args_dict, required, class_checkers):
    """

    :param args_dict: dict of att_names to att_values
    :param required: iterable of attribute names
    :param class_checkers: iterable of ClassChecker instances
    :return: list of errors if any found or empty list otherwise
    """
    return list(
        chain.from_iterable(
            c.check(args_dict, required) for c in class_checkers
        )
    )

def to_bool(value):
    value = str(value).lower()
    if value in ("none", "0", "false"):
        return False
    if value in ("true", "1"):
        return True
    raise ValueError


def check_and_convert(cls, args_dict):
    """

    :param cls: the class to be checked and converted
    :param args_dict: dict of att names to att values
    :return: A checked and converted legal instance
    :raises: IllegalModelStateError if checks or conversions failed
    """
    required = frozenset(getattr(cls, "REQUIRED", []))
    some_ofs = getattr(cls, "SOME_OFS", [])
    converters = getattr(cls, "CONVERTERS", [])
    classes = getattr(cls, "CLASSES", [])

    args = args_dict.copy()
    errors = list(
        chain.from_iterable(
            (
                _check_required(args, required),
                _check_some_ofs(args, some_ofs),
                _check_conversions(args, required, converters),
                _check_classes(args, required, classes),
            )
        )
    )
    if errors:
        msg = "cannot instantiate class : {name}. Got Errors : {errors}"
        raise IllegalModelStateError(msg.format(name=cls.__name__, errors=errors))

    return cls(**args)
