import xmltodict


from vast.parsers import vast_v2
from vast.parsers.shared import ParseError

_PARSERS = {
    u"2.0": vast_v2.parse_xml
}

def from_xml_file(xml_file, **kwargs):
    with open(xml_file, "r") as xml_file_like_object:
        return _parse(xml_file_like_object, **kwargs)


def from_xml_string(xml_input, **kwargs):
    """
    Entry point for parsing a VAST XML into a VAST model
    
    :param xml_input: as str or file like object
    :param kwargs: pass on to xmltodict
    :return: parsed Vast object
    """
    return _parse(xml_input, **kwargs)


def _parse(xml_string_or_file_like_object, **kwargs):
    root = xmltodict.parse(xml_string_or_file_like_object, **kwargs)
    if "VAST" not in root:
        raise ParseError("root must have VAST element")
    vast = root["VAST"]

    if not isinstance(vast, dict):
        raise ParseError("vast must have children elements but was '%s'" % vast)
    version = vast.get("@version")
    if not version:
        raise ParseError("missing version attribute in vast element '%s'" % vast)

    parser = _PARSERS.get(version)
    if parser is None:
        raise ParseError("Cannot parse vast version %s" % version)

    return parser(root)
