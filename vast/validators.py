
def make_type_validator(_type):
    msg_format = "'{name}' must be {type!r} (got {value!r} that is a {actual!r})."

    def validate(value, attr_name, msg=None):
        if not isinstance(value, _type):
            msg = msg or msg_format.format(
                name=attr_name, type=_type,
                actual=value.__class__, value=value
            )
            raise TypeError(msg, attr_name, _type, value)

    return validate


def make_greater_then_validator(must_be_greater_than_me):
    msg_format = "'{name}' must be greater than {gt!r} but got {value!r}."

    def validate(value, attr_name, msg=None):
        if must_be_greater_than_me >= value:
            msg = msg or msg_format.format(
                name=attr_name, gt=must_be_greater_than_me, value=value,
            )
            raise ValueError(msg, attr_name, value)

    return validate


def make_in_validator(_collection):
    collection = set(_collection)

    msg_format = "'{name}' with value {value!r} not found in collection {col!r}."

    def validate(value, attr_name, msg=None):
        if value not in collection:
            msg = msg or msg_format.format(
                name=attr_name, value=value, col=_collection,
            )
            raise ValueError(msg, attr_name, value)

    return validate


def make_compound_validator(*validators):
    def validate(value, attr_name, msg=None):
        for validator_fn in validators:
            validator_fn(value, attr_name, msg=msg)

    return validate


STR_VALIDATOR = make_type_validator(str)
BOOL_VALIDATOR = make_type_validator(bool)
SEMI_POS_VALIDATOR = make_compound_validator(
    make_type_validator(int),
    make_greater_then_validator(-1),
)
POS_VALIDATOR = make_compound_validator(
    make_type_validator(int),
    make_greater_then_validator(0),
)
IN_VALIDATOR = make_in_validator
