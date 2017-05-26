import attr

from vast.models.vast_v2 import Ad, Vast, Wrapper
from vast.parsers import ParseError


@attr.s()
class _ParsedVast(object):
    vast = attr.ib()
    version = attr.ib()
    ad = attr.ib()

    @classmethod
    def from_xml_dict(cls, xml_dict):
        vast = xml_dict.get("VAST")

        error_msg = None
        if not vast:
            error_msg = "Must declare a vast element in xml dict - '%s'"
        elif "@version" not in vast:
            error_msg = "Must declare version attribute in vast - '%s'"
        elif vast["@version"] != "2.0":
            error_msg = "Called vast 2.0 parser on vast with different version-  '%s'"
        elif "Ad" not in vast:
            error_msg = "Must declare Ad element in vast - '%s'"

        if error_msg is not None:
            raise ParseError(error_msg % xml_dict)

        version = vast["@version"]
        ad = _ParsedAd.from_xml_dict(vast["Ad"])

        return cls(vast, version, ad)


@attr.s()
class _ParsedAd(object):
    ad = attr.ib()
    inline = attr.ib()
    wrapper = attr.ib()

    @classmethod
    def from_xml_dict(cls, xml_dict):
        inline, wrapper = None, None
        if "InLine" in xml_dict:
            inline = _ParsedInLine.from_xml_dict(xml_dict["Inline"])
        elif "Wrapper" in xml_dict:
            wrapper = _ParsedWrapper.from_xml_dict(xml_dict["Wrapper"])
        else:
            msg = "Must declare either inline or wrapper in xml_dict '%s'"
            raise ParseError(msg % xml_dict)

        return cls(xml_dict, inline, wrapper)

    @property
    def id(self):
        return self.ad.get("@id")


@attr.s()
class _ParsedWrapper(object):
    wrapper = attr.ib()

    @classmethod
    def from_xml_dict(cls, xml_dict):
        return cls(xml_dict)

    @property
    def vast_ad_tag_uri(self):
        return self.wrapper.get("VASTAdTagURI")

    @property
    def ad_system(self):
        return self.wrapper.get("AdSystem")

    @property
    def ad_title(self):
        return self.wrapper.get("AdTitle")

    @property
    def impression(self):
        return self.wrapper.get("Impression")

    @property
    def error(self):
        return self.wrapper.get("Error")

    @property
    def creatives(self):
        creatives = self.wrapper.get("creatives", {})
        for v in creatives.values():
            yield v


@attr.s()
class _ParsedInLine(object):
    inline = attr.ib()

    @classmethod
    def from_xml_dict(cls, xml_dict):
        return cls(xml_dict)


def parse_xml(root):
    vast = _ParsedVast.from_xml_dict(root)
    ad = vast.ad
    wrapper = ad.wrapper
    inline = ad.inline
    if wrapper:
        return Vast.make(
            version=vast.version,
            ad=Ad.make(
                id=ad.id,
                wrapper=Wrapper.make(
                    ad_system=wrapper.ad_system,
                    vast_ad_tag_uri=wrapper.vast_ad_tag_uri,
                    ad_title=wrapper.ad_title,
                    impression=wrapper.impression,
                    error=wrapper.error,
                    creatives=creatives_from_wrapper(wrapper),
                ),
            ),
        )
    elif inline:
        return Vast.make(
            version=vast.version,
            ad=Ad.make(
                id=ad.id,
                inline=_parse_inline(inline),
            ),
        )
    else:
        raise ParseError("This should never be called but here just in case")


def _parse_inline(inline):
    return inline


def from_creaive_dict(c_dict):
    return None


def creatives_from_wrapper(wrapper):
    return [from_creaive_dict(c) for c in wrapper.creatives] or None


