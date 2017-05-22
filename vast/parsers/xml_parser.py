import xmltodict


from vast.parsers import vast_v2

_parsers = {
    u"2.0": vast_v2.parse_xml
}


class _ParsedVast(object):
    def __init__(self, root):
        self.root = root

    @property
    def version(self):
        return self.root["VAST"]["@version"]

    @property
    def ad(self):
        return self.root["VAST"].get("Ad", {})


def from_xml_string(xml_input, **kwargs):
    root = xmltodict.parse(xml_input, **kwargs)

    vast = _ParsedVast(root)
    version = vast.version
    parser = _parsers.get(version)
    if parser is None:
        raise ValueError("unknown version %s" % version)

    return parser(vast)