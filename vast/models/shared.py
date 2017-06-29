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
    type = attr.ib()
    attr_names = attr.ib()

    def _error(self, attr_name, value):
        msg = "Cannot convert '{attr_name}={value}' to '{type}'"
        return msg.format(
                attr_name=attr_name,
                value=value,
                type=self.type,
            )

    def _convert(self, value):
        # TODO create this via a class method or in init
        if self.type != bool:
            return self.type(value)
        else:
            return to_bool(value)

    def convert(self, args_dict, required):
        errors = []
        for attr_name in self.attr_names:
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


@attr.s()
class ClassChecker(object):
    attr_name = attr.ib()
    clazz = attr.ib()
    is_container = attr.ib(default=False)

    def _check(self, errors, v):
        if not isinstance(v, self.clazz):
            msg = "Attribute {attr_name} is not of class {class_name} but of type {type}"
            errors.append(
                msg.format(
                    attr_name=self.attr_name,
                    class_name=self.clazz.__name__,
                    type=type(v),
                )
            )

    def check(self, args_dict, required):
        errors = []
        value = args_dict.get(self.attr_name)
        if value is None:
            if self.attr_name in required:
                self._check(errors, value)
            return errors

        if not self.is_container:
            self._check(errors, value)
            return errors

        for v in value:
            self._check(errors, v)
        return errors


def _check_required(args_dict, required):
    msg = "Missing required attribute :'{attr_name}'"
    return [
        msg.format(attr_name=attr_name)
        for attr_name in required
        if attr_name not in args_dict
    ]


def _check_conversions(args_dict, required, converters):
    return list(
        chain.from_iterable(
            c.convert(args_dict, required) for c in converters
        )
    )


def _check_some_ofs(args_dict, some_ofs):
    return list(
        chain.from_iterable(
            s.check(args_dict) for s in some_ofs
        )
    )


def _check_classes(args_dict, required, class_checkers):
    return list(
        chain.from_iterable(
            c.check(args_dict, required) for c in class_checkers
        )
    )


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
    def convert(args_dict):
        errors = list(
            chain.from_iterable(
                c.convert(args_dict, required) for c in converters
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
        errors = list(
            chain.from_iterable(
                s.check(args_dict) for s in some_ofs
            )
        )
        return errors

    return checker


def make_class_checker(classes_checkers, required):
    """

    :param classes_checkers: iterable of tuples where
     first element is the class itself
     second element is the attr name that should be instance of that class
     third element is a bool where if true indicates the attr_name is a container
    :param required: set of required fields
    :return: check function which takes in dictionary of kw args
    """

    def check(args_dict):
        errors = list(
            chain.from_iterable(
                c.check(args_dict, required) for c in classes_checkers
            )
        )
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


# TODO start using this instead of decorator ?
def check_and_convert(cls, args_dict, required=None, some_ofs=None, converters=None, classes=None):
    required = required or frozenset(getattr(cls, "REQUIRED", []))
    some_ofs = some_ofs or getattr(cls, "SOME_OFS", [])
    converters = converters or getattr(cls, "CONVERTERS", [])
    classes = classes or getattr(cls, "CLASSES", [])

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
