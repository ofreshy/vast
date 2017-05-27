
class ParseError(Exception):
    pass


def parse_duration(duration_str):
    """

    :param duration_str: format of HH:MM:SS 
    :return: duration in seconds int
    """
    h, m, s = map(int, duration_str.split(":"))
    return h * 3600 + m * m * 60 + s


def unparse_duration(duration_int):
    """

    :param duration_int: in seconds
    :return: in format HH:MM:SS
    """
    d = duration_int
    h, m, s = d / 3600, (d % 3600) / 60, (d % 3600) % 60
    return "%02d:%02d:%02d" % (h, m, s)


def accept_none(parse_func):
    def parse(xml_dict):
        if xml_dict is None:
            return None
        return parse_func(xml_dict)

    return parse


def extract_fields(xml_dict, fields, method="required"):
    if method == "required":
        _check_required_fields(xml_dict, fields)
    elif method == "one_of":
        _check_one_of_fields(xml_dict, fields)
    # else it is optional
    return (xml_dict.get(f) for f in fields)


def _check_one_of_fields(xml_dict, keys):
    found = [k for k in keys if k in xml_dict]
    if len(found) != 1:
        msg = "Only 1 key from {keys} should be found, but found {found} in {xml_dict}"
        raise ParseError(msg.format(keys=keys, found=found, xml_dict=xml_dict))


def _check_required_fields(xml_dict, fields):
    missing = [f for f in fields if not xml_dict.get(f)]
    if missing:
        msg = "Missing required fields : {missing} in {xml_dict}"
        raise ParseError(msg.format(missing=missing, xml_dict=xml_dict))