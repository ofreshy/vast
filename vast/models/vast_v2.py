# -*- coding: utf-8 -*-

import attr

from vast import validators
from vast.validators import (
    BOOL_VALIDATOR,
    MIN_MAX_VALIDATOR,
    POS_INT_VALIDATOR,
    SEMI_POS_INT_VALIDATOR,
    STR_VALIDATOR,
)

DELIVERY = "streaming", "progressive"


DELIVERY_VALIDATOR = validators.make_in_validator(DELIVERY)


@attr.s(frozen=True)
class MediaFile(object):
    """
    2.3.1.4 Media File Attributes
    
    * For media files that have no width and height (such as with an audio-only file), values of 0 are acceptable.
    
    """
    delivery = attr.ib()
    type = attr.ib()
    width = attr.ib()
    height = attr.ib()

    codec = attr.ib()
    id = attr.ib()
    bitrate = attr.ib()
    min_bitrate = attr.ib()
    max_bitrate = attr.ib()
    scalable = attr.ib()
    maintain_aspect_ratio = attr.ib()
    api_framework = attr.ib()

    @classmethod
    def make(cls,
             delivery, type, width, height,
             codec=None, id=None, bitrate=None,
             min_bitrate=None, max_bitrate=None, scalable=True,
             maintain_aspect_ratio=False, api_framework=None,
             ):
        """
        Entry point for making MediaFile instances. 
        
        :param delivery: either “progressive” for progressive download protocols (such as HTTP) 
        or “streaming” for streaming protocols.
        :param type: MIME type for the file container. 
        Popular MIME types include, but are not limited to “video/x- flv” for Flash Video and “video/mp4” for MP4
        :param width: the native width of the video file, in pixels
        :param height: the native height of the video file, in pixels
        :param codec: the codec used to encode the file which can take values as specified by RFC 4281: 
        http://tools.ietf.org/html/rfc4281
        :param id: an identifier for the media file
        :param bitrate: for progressive load video, the bitrate value specifies the average bitrate for the media file;
        :param min_bitrate: used in conjunction with max_bitrate for streaming videos
        :param max_bitrate: used in conjunction with min_bitrate for streaming videos
        :param scalable: identifies whether the media file is meant to scale to larger dimensions
        :param maintain_aspect_ratio: identifies whether aspect ratio for media file is maintained
        :param api_framework: identifies the API needed to execute an interactive media file
        :return: 
        """
        inst = cls(
            delivery, type, width, height,
            codec=codec, id=id, bitrate=bitrate,
            min_bitrate=min_bitrate, max_bitrate=max_bitrate, scalable=scalable,
            maintain_aspect_ratio=maintain_aspect_ratio, api_framework=api_framework,
        )

        DELIVERY_VALIDATOR(delivery, "delivery")
        STR_VALIDATOR(type, "type")
        SEMI_POS_INT_VALIDATOR(width, "width")
        SEMI_POS_INT_VALIDATOR(height, "height")

        if delivery == "progressive":
            POS_INT_VALIDATOR(bitrate, "bitrate")
        elif delivery == "streaming":
            POS_INT_VALIDATOR(min_bitrate, "min_bitrate")
            POS_INT_VALIDATOR(max_bitrate, "max_bitrate")
            MIN_MAX_VALIDATOR((min_bitrate, max_bitrate), "min max bitrate")

        BOOL_VALIDATOR(scalable, "scalable")
        BOOL_VALIDATOR(maintain_aspect_ratio, "maintain_aspect_ratio")

        if codec is not None:
            STR_VALIDATOR(inst, "codec", codec)

        if id is not None:
            STR_VALIDATOR(inst, "id", id)

        if api_framework is not None:
            STR_VALIDATOR(api_framework, "api_framework")

        return inst


@attr.s(frozen=True)
class Creative(object):
    """
    TBD
    """
    pass


CREATIVE_VALIDATOR = validators.make_type_validator(Creative)


@attr.s(frozen=True)
class InLine(object):
    """
    2.2.4 The <InLine> Element
    The last ad server in the ad supply chain serves an <InLine> element. Within the nested elements of an <InLine> element are all the files and URIs necessary to display the ad.
    2.2.4.1 Required InLine Elements
    Contained directly within the <InLine> element are the following required elements:
    • <AdSystem>: the name of the ad server that returned the ad
    • <AdTitle>: the common name of the ad
    • <Impression>: a URI that directs the video player to a tracking resource file that the video player
    should request when the first frame of the ad is displayed
    • <Creatives>: the container for one or more <Creative> elements
    """
    ad_system = attr.ib()
    ad_title = attr.ib()
    impression = attr.ib()
    creatives = attr.ib()

    @classmethod
    def make(cls, ad_system, ad_title, impression, creatives):
        STR_VALIDATOR(ad_system)
        STR_VALIDATOR(ad_title)
        STR_VALIDATOR(impression)
        if not creatives:
            raise TypeError
        if not isinstance(creatives, (list, set, tuple)):
            raise TypeError
        for creative in creatives:
            CREATIVE_VALIDATOR(creative)

        return cls(ad_system, ad_title, impression, creatives)


@attr.s(frozen=True)
class Wrapper(object):
    """
    
    """
    ad_system = attr.ib()
    vast_ad_tag_uri = attr.ib()
    ad_title = attr.ib()
    impression = attr.ib()
    error = attr.ib()
    creatives = attr.ib()

    @classmethod
    def make(cls, ad_system, vast_ad_tag_uri,
             ad_title=None, impression=None, error=None, creatives=None,
             ):
        STR_VALIDATOR(ad_system)
        STR_VALIDATOR(vast_ad_tag_uri)
        if ad_title is not None:
            STR_VALIDATOR(ad_title)
        if impression is not None:
            STR_VALIDATOR(impression)
        if error is not None:
            STR_VALIDATOR(error)
        if creatives is not None:
            for c in creatives:
                CREATIVE_VALIDATOR(c)

        return cls(ad_system, vast_ad_tag_uri, ad_title, impression, error, creatives)
