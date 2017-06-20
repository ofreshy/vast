# -*- coding: utf-8 -*-

"""
Models for the VAST 2.0 Version 

Models are intentionally simple containers with very little logic. 

Models are not meant to be created directly via __init__ method.
Instead use the 'make' class method provided.
This to make sure that created models adhere to vast spec. 
"""
import attr
from enum import Enum

from vast import validators
from vast.models.shared import with_checker_converter


class Delivery(Enum):
    """
    either
    “progressive” for progressive download protocols (such as HTTP)
    or
    “streaming” for streaming protocols.
    """
    STREAMING = "streaming"
    PROGRESSIVE = "progressive"


class ApiFramework(Enum):
    """
    The API necessary to communicate with the creative if available
    """
    VPAID = "VPAID"


class MimeType(Enum):
    """
     MIME type for the file container.
     Popular MIME types include, but are not limited to
     “video/x- flv” for Flash Video and “video/mp4” for MP4
    """
    MP4 = "video/mp4"
    JS = "application/javascript"
    FLASH = "application/x-shockwave-flash"
    WEBM = "video/webm"
    GPP = "video/3gpp"
    MPEG = "application/x-mpegURL"


class TrackingEventType(Enum):
    """
    Event Types for User interaction with the Creative
    """
    CREATIVE_VIEW = "creativeView"
    START = "start"
    FIRST_QUARTILE = "firstQuartile"
    MID_POINT = "midpoint"
    THIRD_QUARTILE = "thirdQuartile"
    COMPLETE = "complete"
    MUTE = "mute"
    UNMUTE = "unmute"
    PAUSE = "pause"
    REWIND = "rewind"
    RESUME = "resume"
    FULL_SCREEN = "fullscreen"
    EXPAND = "expand"
    COLLAPSE = "collapse"
    ACCEPT_INVITATION = "acceptInvitation"
    CLOSE = "close"



@with_checker_converter()
@attr.s(frozen=True)
class TrackingEvent(object):
    """
    Event for user interaction with the Creative
    """

    REQUIRED = ("tracking_event_uri", "tracking_event_type")
    CONVERTERS = (
        (unicode, ("tracking_event_uri", )),
        (TrackingEventType, ("tracking_event_type", ))
    )

    tracking_event_uri = attr.ib()
    tracking_event_type = attr.ib()

    @classmethod
    def make(cls, tracking_event_uri, tracking_event_type):
        instance =  cls.check_and_convert(
            args_dict=dict(
                tracking_event_uri=tracking_event_uri,
                tracking_event_type=tracking_event_type,
            ),
        )
        return instance


@with_checker_converter()
@attr.s(frozen=True)
class MediaFile(object):
    """
    2.3.1.4 Media File Attributes
        
    """
    REQUIRED = ("asset", "delivery", "type", "width", "height")
    CONVERTERS = (
        (unicode, ("asset", "codec", "id")),
        (int, ("width", "height", "bitrate", "min_bitrate", "max_bitrate")),
        (bool, ("scalable", "maintain_aspect_ratio")),
        (MimeType, ("type", )),
        (ApiFramework, ("api_framework",)),
        (Delivery, ("delivery", ))
    )

    VALIDATORS = (
        validators.make_greater_then_validator("height", 0),
        validators.make_greater_then_validator("width", 0),
    )


    asset = attr.ib()
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
    def make(
            cls,
            asset, delivery, type, width, height,
            codec=None, id=None, bitrate=None, min_bitrate=None, max_bitrate=None,
            scalable=None, maintain_aspect_ratio=None, api_framework=None,
    ):
        """
            Entry point for making MediaFile instances.

            :param asset: the url to the asset
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
        instance = cls.check_and_convert(
            args_dict=dict(
                asset=asset,
                delivery=delivery,
                type=type,
                width=width,
                height=height,
                codec=codec,
                id=id,
                bitrate=bitrate,
                min_bitrate=min_bitrate,
                max_bitrate=max_bitrate,
                scalable=scalable,
                maintain_aspect_ratio=maintain_aspect_ratio,
                api_framework=api_framework,
            ),
        )

        if instance.type in (MimeType.FLASH, MimeType.JS):
            vs = list(cls.VALIDATORS)
        elif instance.delivery == Delivery.PROGRESSIVE:
            vs = list(cls.VALIDATORS) + [cls._validate_bitrate]
        else:
            vs = list(cls.VALIDATORS) + [cls._validate_min_max_bitrate]

        validators.validate(instance, vs)

        return instance

    @staticmethod
    def _validate_bitrate(instance):
        if instance.bitrate is None:
            return "media file bitrate cannot be None for progressive media"
        if instance.bitrate < 0:
            return "media file bitrate must be > 0 but was %s" % instance.bitrate

    @staticmethod
    def _validate_min_max_bitrate(instance):
        errors = []
        if instance.min_bitrate is None:
            errors.append("media file min_bitrate cannot be None for streaming media")
        if instance.max_bitrate is None:
            errors.append("media file min_bitrate cannot be None for streaming media")
        if not errors and instance.min_bitrate > instance.max_bitrate:
            msg = "media file min_bitrate={min_bitrate} is greater than max_bitrate={max_bitrate}"
            errors.append(msg.format(min_bitrate=instance.min_bitrate, max_bitrate=instance.max_bitrate))
        return ",".join(errors) or None


@with_checker_converter()
@attr.s(frozen=True)
class LinearCreative(object):
    """
    The most common type of video advertisement trafficked in the industry is a “linear ad”,
    which is an ad  that displays in the same area as the content but not at the same time as the content.
    In fact, the video  player must interrupt the content before displaying a linear ad.
    Linear ads are often displayed right  before the video content plays.
    This ad position is called a “predroll” position.
    For this reason, a linear ad  is often called a “predroll.”
    
    A <Linear> element has two required child elements, the <Duration> and the <MediaFiles>  element. 
    Additionally three optional child elements are offered: 
    <VideoClicks>, <AdParameters> and <TrackingEvents>. 
    """
    REQUIRED = ("duration", "media_files")
    CONVERTERS = [(int, ("duration", ))]
    CLASSES = (
        ("media_files", MediaFile, True),
        ("tracking_events", TrackingEvent, True),
    )
    VALIDATORS = (
        validators.make_greater_then_validator("duration", 0, False),
    )

    duration = attr.ib()
    media_files = attr.ib()
    video_clicks = attr.ib()
    ad_parameters = attr.ib()
    tracking_events = attr.ib()

    @classmethod
    def make(cls, duration, media_files, video_clicks=None, ad_parameters=None, tracking_events=None):
        instance = cls.check_and_convert(
            args_dict=dict(
                duration=duration,
                media_files=media_files,
                video_clicks=video_clicks,
                ad_parameters=ad_parameters,
                tracking_events=tracking_events,
            ),
        )
        validators.validate(instance)

        return instance

    def as_dict(self):
        from collections import OrderedDict
        return attr.asdict(self, dict_factory=OrderedDict, retain_collection_types=True)


@with_checker_converter()
@attr.s(frozen=True)
class Creative(object):
    """
    A creative in VAST is a file that is part of a VAST ad.
    Multiple creative may be provided in the form of  Linear, NonLinear, or Companions.
    Multiple creative of the same kind may also be provided in different
    technical formats so that the file most suited to the user’s device can be displayed
     (only the creative best suited to the technology/device would be used in this case).
    Despite how many or what type of  creative are included as part of the Ad,
    all creative files should generally represent the same creative  concept.
    Within the <InLine> element is one <Creatives> element.
    The <Creatives> element provides  details about the files for each creative to be included as part of the ad experience.
    Multiple  <Creative> may be nested within the <Creatives> element.
    Note the plural spelling of the primary  element <Creatives> and the singular spelling of the nested element <Creative>.
    Each nested <Creative> element contains one of: <Linear>, <NonLinear> or <CompanionAds>.

    The following attributes are available for the <Creative> element:
    • id: an ad server-defined identifier for the creative
    • sequence: the numerical order in which each sequenced creative should display
        (not to be confused with the <Ad> sequence attribute used to define Ad Pods)
    • adId: identifies the ad with which the creative is served
    • apiFramework: the technology used for any included API
    All creative attributes are optional.
    """

    SOME_OFS = (
        (("linear", "non_linear", "companion_ads"), 2),
    )
    CONVERTERS = (
        (unicode, ("id", "ad_id")),
        (ApiFramework, ("api_framework",)),
        (int, ("sequence",))
    )
    CLASSES = (
        ("linear", LinearCreative, False),
    )
    VALIDATORS = (
        validators.make_greater_then_validator("sequence", -1),
    )

    linear = attr.ib()
    non_linear = attr.ib()
    companion_ads = attr.ib()

    id = attr.ib()
    sequence = attr.ib()
    ad_id = attr.ib()
    api_framework = attr.ib()

    @classmethod
    def make(cls, linear=None, non_linear=None, companion_ads=None,
             id=None, sequence=None, ad_id=None, api_framework=None,
             ):
        instance = cls.check_and_convert(
            args_dict=dict(
                linear=linear,
                non_linear=non_linear,
                companion_ads=companion_ads,
                id=id,
                sequence=sequence,
                ad_id=ad_id,
                api_framework=api_framework,
            ),
        )
        validators.validate(instance, cls.VALIDATORS)

        return instance


@with_checker_converter()
@attr.s(frozen=True)
class Inline(object):
    """
    2.2.4 The <InLine> Element
    The last ad server in the ad supply chain serves an <InLine> element. 
    Within the nested elements of an <InLine> element are all the files and URIs necessary to display the ad.
    2.2.4.1 Required InLine Elements
    Contained directly within the <InLine> element are the following required elements:
    • <AdSystem>: the name of the ad server that returned the ad
    • <AdTitle>: the common name of the ad
    • <Impression>: a URI that directs the video player to a tracking resource file that the video player
    should request when the first frame of the ad is displayed
    • <Creatives>: the container for one or more <Creative> elements
    """
    REQUIRED = ("ad_system", "ad_title", "impression", "creatives")
    CONVERTERS = ((unicode, ("ad_system", "ad_title", "impression")), )
    CLASSES = (("creatives", Creative, True), )

    ad_system = attr.ib()
    ad_title = attr.ib()
    impression = attr.ib()
    creatives = attr.ib()

    @classmethod
    def make(cls, ad_system, ad_title, impression, creatives):
        instance = cls.check_and_convert(
            args_dict=dict(
                ad_system=ad_system,
                ad_title=ad_title,
                impression=impression,
                creatives=creatives,
            ),
        )
        return instance



@with_checker_converter()
@attr.s(frozen=True)
class Wrapper(object):
    """
    
    """
    REQUIRED = ("ad_system", "vast_ad_tag_uri")
    CONVERTERS= ((unicode, ("ad_system", "ad_title", "impression", "error")), )
    CLASSES = (("creatives", Creative, True), )

    ad_system = attr.ib()
    vast_ad_tag_uri = attr.ib()
    ad_title = attr.ib()
    impression = attr.ib()
    error = attr.ib()
    creatives = attr.ib()

    @classmethod
    def make(cls, ad_system, vast_ad_tag_uri, ad_title=None, impression=None, error=None, creatives=None):
        instance = cls.check_and_convert(
            args_dict=dict(
                ad_system=ad_system,
                vast_ad_tag_uri=vast_ad_tag_uri,
                ad_title=ad_title,
                impression=impression,
                error=error,
                creatives=creatives,
            ),
        )
        return instance


@with_checker_converter()
@attr.s(frozen=True)
class Ad(object):
    """
    
    """
    REQUIRED = ("id", )
    SOME_OFS = ((("wrapper", "inline"), 1), )
    CONVERTERS = ((unicode, ("id", )), )

    id = attr.ib()
    wrapper = attr.ib()
    inline = attr.ib()

    @classmethod
    def make(cls, id, wrapper=None, inline=None):
        instance = cls.check_and_convert(
            args_dict=dict(
                id=id,
                wrapper=wrapper,
                inline=inline,
            ),
        )
        return instance

    @classmethod
    def make_wrapper(cls, id, wrapper):
        return cls.make(id=id, wrapper=wrapper)

    @classmethod
    def make_inline(cls, id, inline):
        return cls.make(id=id, inline=inline)


@with_checker_converter()
@attr.s(frozen=True)
class Vast(object):
    """
    The Document Root Element
    """
    REQUIRED = ("version", "ad")
    CLASSES = (("ad", Ad, False), )

    version = attr.ib()
    ad = attr.ib()

    @classmethod
    def make(cls, version, ad):
        instance = cls.check_and_convert(
            args_dict=dict(
                version=version,
                ad=ad,
            ),
        )
        validators.validate(instance, [cls._validate_version])

        return instance

    @staticmethod
    def _validate_version(instance):
        if instance.version != "2.0":
            msg = "version must be 2.0 for vast 2 instance and was '{version}'"
            return msg.format(version=instance.version)
