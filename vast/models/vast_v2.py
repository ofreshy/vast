# -*- coding: utf-8 -*-

import attr

from vast import validators
from vast.validators import (
    BOOL_VALIDATOR,
    POS_VALIDATOR,
    SEMI_POS_VALIDATOR,
    STR_VALIDATOR,
)

DELIVERY = "streaming", "progressive"


DELIVERY_VALIDATOR = validators.make_in_validator(DELIVERY)


@attr.s(frozen=True)
class MediaFile(object):
    """
    2.3.1.4 Media File Attributes
    
    * For media files that have no width and height (such as with an audio-only file), values of “0” are acceptable.
    
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

    attribs = ("a", "b")

    @classmethod
    def make(cls,
             delivery, type, width, height,
             codec=None, id=None, bitrate=None,
             min_bitrate=None, max_bitrate=None, scalable=True,
             maintain_aspect_ratio=False, api_framework=None,
             ):
        """
        Entry point for class, making sure that all fields are valid
        
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
        SEMI_POS_VALIDATOR(width, "width")
        SEMI_POS_VALIDATOR(height, "height")

        if delivery == "progressive":
            POS_VALIDATOR(bitrate, "bitrate")
        elif delivery == "streaming":
            POS_VALIDATOR(min_bitrate, "min_bitrate")
            POS_VALIDATOR(max_bitrate, "max_bitrate")

        BOOL_VALIDATOR(scalable, "scalable")
        BOOL_VALIDATOR(maintain_aspect_ratio, "maintain_aspect_ratio")

        if codec is not None:
            STR_VALIDATOR(inst, "codec", codec)

        if id is not None:
            STR_VALIDATOR(inst, "id", id)

        if api_framework is not None:
            STR_VALIDATOR(api_framework, "api_framework")

        return inst

m = MediaFile.make("streaming", "g", 0, 9, min_bitrate=10, max_bitrate=100)
