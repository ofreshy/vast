from vast.models import vast_v2 as v2_models
from vast.parsers.shared import (
    accept_none,
    accept_falsy,
    parse_duration,
)


def parse_xml(xml_dict):
    """

    :param xml_dict: as provided by xml to dict parser
    :return: Vast object if parsing was successful
    """
    return _parse_vast(xml_dict.get("VAST"))


def _parse_vast(xml_dict):
    return v2_models.Vast.make(
        version=xml_dict.get("@version"),
        ad=_parse_ad(xml_dict.get("Ad")),
    )


@accept_none
def _parse_ad(xml_dict):
    return v2_models.Ad.make(
        id=xml_dict.get("@id"),
        inline=_parse_inline(xml_dict.get("InLine")),
        wrapper=_parse_wrapper(xml_dict.get("Wrapper")),
    )


@accept_none
def _parse_wrapper(xml_dict):
    return v2_models.Wrapper.make(
        ad_system=xml_dict.get("AdSystem"),
        vast_ad_tag_uri=xml_dict.get("VASTAdTagURI"),
        ad_title=xml_dict.get("AdTitle"),
        impression=xml_dict.get("Impression"),
        error=xml_dict.get("Error"),
        creatives=_parse_creatives(xml_dict.get("Creatives")),
    )


@accept_none
def _parse_inline(xml_dict):
    return v2_models.Inline.make(
        ad_system=xml_dict.get("AdSystem"),
        ad_title=xml_dict.get("AdTitle"),
        impression=xml_dict.get("Impression"),
        creatives=_parse_creatives(xml_dict.get("Creatives")),
    )


@accept_falsy
def _parse_creatives(creatives):
    return [_parse_creative(c) for c in creatives[0]["Creative"]]


def _parse_creative(xml_dict):
    return v2_models.Creative.make(
        linear=_parse_linear_creative(xml_dict.get("Linear")),
        non_linear=_parse_non_linear_creative(xml_dict.get("NonLinear")),
        companion_ads=_parse_companion_ads_creative(xml_dict.get("CompanionAds")),
        id=xml_dict.get("@id"),
        sequence=xml_dict.get("@sequence"),
        ad_id=xml_dict.get("@adId"),
        api_framework=xml_dict.get("@apiFramework"),
    )


@accept_none
def _parse_linear_creative(xml_dict):
    return v2_models.LinearCreative.make(
        duration=parse_duration(xml_dict.get("Duration")),
        media_files=_parse_media_files(xml_dict.get("MediaFiles")),
        video_clicks=_parse_video_clicks(xml_dict.get("VideoClicks")),
        ad_parameters=_parse_ad_parameters(xml_dict.get("AdParameters")),
        tracking_events=_parse_tracking_events(xml_dict.get("TrackingEvents")),
    )


@accept_none
def _parse_non_linear_creative(xml_dict):
    # TODO
    pass


@accept_none
def _parse_companion_ads_creative(xml_dict):
    # TODO
    pass


@accept_none
def _parse_video_clicks(xml_dict):
    return v2_models.VideoClicks.make(
        click_through=xml_dict.get("ClickThrough"),
        click_tracking=xml_dict.get("ClickTracking"),
        custom_click=xml_dict.get("CustomClick"),
    )


@accept_none
def _parse_ad_parameters(xml_dict):
    return v2_models.AdParameters.make(
        data=xml_dict.get("#text"),
        xml_encoded=xml_dict.get("@xmlEncoded"),
    )


@accept_falsy
def _parse_media_files(media_files):
    return [_parse_media_file(mf) for mf in media_files[0]["MediaFile"]]


def _parse_media_file(xml_dict):
    return v2_models.MediaFile.make(
        asset=xml_dict.get("#text"),
        delivery=xml_dict.get("@delivery"),
        type=xml_dict.get("@type"),
        width=xml_dict.get("@width"),
        height=xml_dict.get("@height"),
        bitrate=xml_dict.get("@bitrate"),
        min_bitrate=xml_dict.get("@minBitrate"),
        max_bitrate=xml_dict.get("@maxBitrate"),
        scalable=xml_dict.get("@scalable"),
        maintain_aspect_ratio=xml_dict.get("@maintainAspectRatio"),
        api_framework=xml_dict.get("@apiFramework"),
    )


@accept_falsy
def _parse_tracking_events(tracking_events):
    return [_parse_tracking_event(t) for t in tracking_events[0]["Tracking"]]


def _parse_tracking_event(xml_dict):
    return v2_models.TrackingEvent.make(
        tracking_event_uri=xml_dict.get("#text"),
        tracking_event_type=xml_dict.get("@event"),
    )
