import xmltodict

from vast.parsers import ParseError

from vast.parsers import vast_v2

_PARSERS = {
    u"2.0": vast_v2.parse_xml
}


def from_xml_string(xml_input, **kwargs):
    root = xmltodict.parse(xml_input, **kwargs)
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
