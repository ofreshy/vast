from collections import defaultdict

from vast.models.vast_v2 import Ad, Vast, Wrapper
from vast.parsers import ParseError


class _ParsedAd(object):
    def __init__(self, ad):
        self.ad = ad

    @property
    def id(self):
        return self.ad.get("@id")

    @property
    def inline(self):
        return self.ad.get("Inline")

    @property
    def wrapper(self):
        return self.ad.get("Wrapper")


class _ParsedWrapper(object):
    def __init__(self, wrapper_dict):
        self.wrapper_dict = wrapper_dict

    @property
    def vast_ad_tag_uri(self):
        return self.wrapper_dict.get("VASTAdTagURI")

    @property
    def ad_system(self):
        return self.wrapper_dict.get("AdSystem")

    @property
    def ad_title(self):
        return self.wrapper_dict.get("AdTitle")

    @property
    def impression(self):
        return self.wrapper_dict.get("Impression")

    @property
    def error(self):
        return self.wrapper_dict.get("Error")

    @property
    def creatives(self):
        creatives = self.wrapper_dict.get("creatives", {})
        for v in creatives.values():
            yield v


class _ParsedInLine(object):
    def __init__(self, root):
        self._root = root
        ad = root["VAST"].get("Ad", {})
        self._inline = ad.get("InLine", {})

    @property
    def mimetypes(self):
        mimetypes = set([])
        for media_file in self.media_files:
            mimetype = media_file["@type"]
            if mimetype not in mimetypes:
                yield mimetype
            mimetypes.add(mimetype)

    @property
    def mime_to_bitrates(self):
        mime_to_bitrates = defaultdict(list)
        for media_file in self.media_files:
            mimetype = media_file["@type"]
            bitrate = media_file.get("@bitrate")
            if bitrate:
                mime_to_bitrates[mimetype].append(int(bitrate))

        for mime_type, bitrates in mime_to_bitrates.items():
            mime_to_bitrates[mime_type] = sorted(bitrates)

        return mime_to_bitrates

    @property
    def mime_to_sizes(self):
        mime_to_sizes = defaultdict(set)
        for media_file in self.media_files:
            mimetype = media_file["@type"]
            width, height = media_file.get("@width"), media_file.get("@height")
            if width and height:
                size = (int(width), int(height))
                mime_to_sizes[mimetype].add(size)

        for mime_type, values in mime_to_sizes.items():
            mime_to_sizes[mime_type] = sorted(list(values))

        return mime_to_sizes

    @property
    def creatives(self):
        # only interested in Linear right now
        creatives = self._inline.get("Creatives", {})
        for v in creatives.values():
            if "Linear" in v:
                yield v["Linear"]

    @property
    def media_files(self):
        for creative in self.creatives:
            for media_file in creative.get("MediaFiles", {}).get("MediaFile"):
                yield media_file

    @property
    def durations(self):
        for creative in self.creatives:
            yield creative["Duration"]

    @property
    def duration(self):
        return next(self.durations, None)


def parse_xml(parsed_vast):
    version = parsed_vast.version
    ad = _ParsedAd(parsed_vast.ad)

    if ad.wrapper:
        return Vast.make(
            version=version,
            ad=Ad.make(
                id=ad.id,
                wrapper=_parse_wrapper(ad),
            ),
        )
    elif ad.inline:
        return Vast.make(
            version=version,
            ad=Ad.make(
                id=ad.id,
                inline=_parse_inline(ad),
            ),
        )
    else:
        raise ParseError("Must provide either Wrapper or Inline element in ad '%s'" % parsed_vast.ad)


def _parse_wrapper(ad):
    wrapper = _ParsedWrapper(ad.wrapper)
    ad_system = wrapper.ad_system
    vast_ad_tag_uri = wrapper.vast_ad_tag_uri

    ad_title = wrapper.ad_title
    impression = wrapper.impression
    error = wrapper.error

    creatives = [from_creaive_dict(c) for c in wrapper.creatives] or None

    wrapper_model = Wrapper.make(
        ad_system=ad_system,
        vast_ad_tag_uri=vast_ad_tag_uri,
        ad_title=ad_title,
        impression=impression,
        error=error,
        creatives=creatives,
    )
    return wrapper_model


def _parse_inline(ad):
    inline = _ParsedInLine(ad.inline)
    return inline


def from_creaive_dict(c_dict):
    return None

