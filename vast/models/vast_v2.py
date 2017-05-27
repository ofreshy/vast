# -*- coding: utf-8 -*-

import attr

from vast import validators
from vast.validators import (
    BOOL_VALIDATOR,
    MIN_MAX_VALIDATOR,
    POS_INT_VALIDATOR,
    SEMI_POS_INT_VALIDATOR,
    STR_VALIDATOR,
    UNICODE_VALIDATOR,
)

DELIVERY = "streaming", "progressive"


DELIVERY_VALIDATOR = validators.make_in_validator(DELIVERY)


@attr.s(frozen=True)
class MediaFile(object):
    """
    2.3.1.4 Media File Attributes
    
    * For media files that have no width and height (such as with an audio-only file), values of 0 are acceptable.
    
    """
    asset = attr.ib(validator=attr.validators.instance_of(unicode))
    delivery = attr.ib(validator=attr.validators.in_(("progressive", "streaming")))
    type = attr.ib(validator=attr.validators.instance_of(unicode))
    width = attr.ib(convert=int, validator=attr.validators.instance_of(int))
    height = attr.ib(convert=int, validator=attr.validators.instance_of(int))

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
             asset,
             delivery, type, width, height,
             codec=None, id=None, bitrate=None,
             min_bitrate=None, max_bitrate=None, scalable=True,
             maintain_aspect_ratio=False, api_framework=None,
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
        UNICODE_VALIDATOR(asset, "asset")
        DELIVERY_VALIDATOR(delivery, "delivery")
        UNICODE_VALIDATOR(type, "type")
        width, height = map(int, (width, height))
        SEMI_POS_INT_VALIDATOR(width, "width")
        SEMI_POS_INT_VALIDATOR(height, "height")

        if delivery == "progressive":
            bitrate = int(bitrate)
            POS_INT_VALIDATOR(bitrate, "bitrate")
        elif delivery == "streaming":
            min_bitrate, max_bitrate = map(int, (min_bitrate, max_bitrate))
            POS_INT_VALIDATOR(min_bitrate, "min_bitrate")
            POS_INT_VALIDATOR(max_bitrate, "max_bitrate")
            MIN_MAX_VALIDATOR((min_bitrate, max_bitrate), "min max bitrate")

        if scalable is not None:
            BOOL_VALIDATOR(scalable, "scalable")
        else:
            scalable = True

        if maintain_aspect_ratio is not None:
            BOOL_VALIDATOR(maintain_aspect_ratio, "maintain_aspect_ratio")
        else:
            maintain_aspect_ratio = False

        if codec is not None:
            UNICODE_VALIDATOR(codec, "codec")

        if id is not None:
            UNICODE_VALIDATOR(id, "id")

        if api_framework is not None:
            UNICODE_VALIDATOR(api_framework, "api_framework")

        return cls(
            asset,
            delivery, type, width, height,
            codec=codec, id=id, bitrate=bitrate,
            min_bitrate=min_bitrate, max_bitrate=max_bitrate, scalable=scalable,
            maintain_aspect_ratio=maintain_aspect_ratio, api_framework=api_framework,
        )


API_FRAMEWORKS = "VPAID",
API_FRAMEWORKS_VALIDATOR = validators.make_in_validator(API_FRAMEWORKS)


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

    # This is basically a one of - since there are not many types, we specify them all
    linear = attr.ib()
    non_linear = attr.ib()
    companion_ads = attr.ib()

    id = attr.ib()
    sequence = attr.ib()
    ad_id = attr.ib()
    api_framework = attr.ib()

    @classmethod
    def make(cls,
             linear=None, non_linear=None, companion_ad=None,
             id=None, sequence=None, ad_id=None, api_framework=None,
             ):
        if all(x is None for x in (linear, non_linear, companion_ad)):
            raise ValueError("Must specify either inline, non_linear or companion_ad")

        # Add type checks here for ad_type
        if id is not None:
            STR_VALIDATOR(id, "id")
        if sequence is not None:
            SEMI_POS_INT_VALIDATOR(sequence, "sequence")
        if ad_id is not None:
            STR_VALIDATOR(ad_id, "ad_id")
        if api_framework is not None:
            API_FRAMEWORKS_VALIDATOR(api_framework, "api_framework")

        return cls(linear, non_linear, companion_ad, id, sequence, ad_id, api_framework)


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
    # REQUIRED
    duration = attr.ib()
    media_files = attr.ib()

    # OPTIONAL
    video_clicks = attr.ib()
    ad_parameters = attr.ib()
    tracking_events = attr.ib()

    @classmethod
    def make(cls, duration, media_files, video_clicks=None, ad_parameters=None, tracking_events=None):
        POS_INT_VALIDATOR(duration, "duration")

        # TODO add check for media files

        if video_clicks is not None:
            # TODO add checks
            pass
        if ad_parameters is not None:
            # TODO add checks
            pass
        if tracking_events is not None:
            # TODO add checks
            pass
        return cls(duration, media_files, video_clicks, ad_parameters, tracking_events)


CREATIVE_VALIDATOR = validators.make_type_validator(Creative)


@attr.s(frozen=True)
class InLine(object):
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
    # REQUIRED
    ad_system = attr.ib()
    ad_title = attr.ib()
    impression = attr.ib()
    creatives = attr.ib()

    @classmethod
    def make(cls, ad_system, ad_title, impression, creatives):
        UNICODE_VALIDATOR(ad_system, "ad_system")
        UNICODE_VALIDATOR(ad_title, "ad_title")
        UNICODE_VALIDATOR(impression, "impression")
        if not creatives:
            raise ValueError("Creatives must be provided")
        if not isinstance(creatives, (list, set, tuple)):
            raise TypeError
        for creative in creatives:
            CREATIVE_VALIDATOR(creative, "creative")

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
        UNICODE_VALIDATOR(ad_system, "ad_system")
        UNICODE_VALIDATOR(vast_ad_tag_uri, "vast_ad_tag_uri")
        if ad_title is not None:
            UNICODE_VALIDATOR(ad_title, "ad_title")
        if impression is not None:
            UNICODE_VALIDATOR(impression, "impression")
        if error is not None:
            UNICODE_VALIDATOR(error, "error")
        if creatives is not None:
            for c in creatives:
                CREATIVE_VALIDATOR(c, "creative")

        return cls(ad_system, vast_ad_tag_uri, ad_title, impression, error, creatives)


WRAPPER_VALIDATOR = validators.make_type_validator(Wrapper)
INLINE_VALIDATOR = validators.make_type_validator(InLine)


@attr.s(frozen=True)
class Ad(object):
    """
    
    """
    id = attr.ib()
    wrapper = attr.ib()
    inline = attr.ib()

    @classmethod
    def make(cls, id, wrapper=None, inline=None):
        """
        
        :param id: 
        :param wrapper: 
        :param inline: 
        :return: 
        """
        UNICODE_VALIDATOR(id, "id")
        if wrapper is not None:
            WRAPPER_VALIDATOR(wrapper, "wrapper")
        elif inline is not None:
            INLINE_VALIDATOR(inline, "inline")
        else:
            raise ValueError("Must provide either wrapper or inline")

        return cls(id, wrapper, inline)


AD_VALIDATOR = validators.make_type_validator(Ad)
VERSIONS = "2.0", "3.0"
VERSION_VALIDATOR = validators.make_in_validator(VERSIONS)


@attr.s(frozen=True)
class Vast(object):
    """
    The Document Root Element
    """

    version = attr.ib()
    ad = attr.ib()

    @classmethod
    def make(cls, version, ad):
        VERSION_VALIDATOR(version, "version")
        AD_VALIDATOR(ad, "ad")
        return cls(version, ad)
