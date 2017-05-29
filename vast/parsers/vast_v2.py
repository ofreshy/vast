from vast.models import vast_v2 as v2_models
from vast.parsers.shared import (
    accept_none,
    extract_fields,
    parse_duration,
    ParseError,
    to_bool,
)


def parse_xml(xml_dict):
    vast,  = extract_fields(xml_dict, ("VAST",))
    # TODO add here maybe allow for empty
    return parse_vast(vast)


def parse_vast(xml_dict):
    required_fields = ("@version", "Ad")
    version, ad = extract_fields(xml_dict, required_fields)
    return v2_models.make_vast(
        version=version,
        ad=parse_ad(ad),
    )


def parse_ad(xml_dict):
    one_of_fields = ("Wrapper", "InLine")
    wrapper, inline = extract_fields(xml_dict, one_of_fields, method="one_of")
    return v2_models.make_ad(
        id=xml_dict.get("@id"),
        inline=parse_inline(inline),
        wrapper=parse_wrapper(wrapper),
    )


@accept_none
def parse_wrapper(xml_dict):
    required_fields = ("AdSystem", "Impression", "VASTAdTagURI")
    ad_system, impression, vast_ad_tag_uri = extract_fields(
        xml_dict,
        required_fields,
    )

    return v2_models.make_wrapper(
        ad_system=ad_system,
        ad_title=xml_dict.get("AdTitle"),
        impression=impression,
        vast_ad_tag_uri=vast_ad_tag_uri,
        error=xml_dict.get("Error"),
        creatives=parse_creatives(xml_dict.get("Creatives")),
    )


@accept_none
def parse_inline(xml_dict):
    required_fields = ("AdSystem", "AdTitle", "Impression", "Creatives")
    ad_system, ad_title, impression, creatives = extract_fields(xml_dict, required_fields)

    creatives = parse_creatives(creatives)
    if not creatives:
        msg = "InLine element must have at least one creative in {xml_dict}"
        raise ParseError(msg.format(xml_dict))

    return v2_models.make_inline(
        ad_system=ad_system,
        ad_title=ad_title,
        impression=impression,
        creatives=creatives,
    )


@accept_none
def parse_creatives(xml_dict):
    creatives, = extract_fields(xml_dict, ("Creative",))

    if isinstance(creatives, dict):
        return [parse_creative(creatives)]
    if isinstance(creatives, list):
        return [parse_creative(c) for c in creatives]


def parse_creative(xml_dict):
    # This is not exactly one of.
    # At least one should be present but companion ads can show up with any
    one_of_fields = ("Linear", "CompanionAds", "NonLinear")
    linear, non_linear, companion_ads = extract_fields(xml_dict, one_of_fields, method="one_of")
    if linear:
        one_of = linear
        linear = parse_linear_creative(linear)
    elif companion_ads:
        one_of = companion_ads
        # TODO add me
        pass
    elif non_linear:
        one_of = non_linear
        # TODO add me
        pass
    else:
        msg = "creative must have either Linear or CompanionAds or NonLinear elements - '%s')"
        raise ParseError(msg % xml_dict)

    # Add shared fields
    optional_fields = ("@id", "@sequence", "AdId", "@api_framework")
    _id, sequence, ad_id, api_framework = extract_fields(one_of, optional_fields, method="optional")

    return v2_models.make_creative(
        linear=linear,
        non_linear=non_linear,
        companion_ad=companion_ads,
        id=_id,
        sequence=sequence,
        ad_id=ad_id,
        api_framework=api_framework,
    )


@accept_none
def parse_linear_creative(xml_dict):
    required_fields = ("Duration", "MediaFiles")
    duration, media_files = extract_fields(xml_dict, required_fields)

    media_files = parse_media_files(media_files)
    if not media_files:
        msg = "Must have at least one media file in {xml_dict}"
        raise ParseError(msg.format(xml_dict=xml_dict))

    tracking_events = xml_dict.get("TrackingEvents")

    return v2_models.make_linear_creative(
        duration=parse_duration(duration),
        media_files=media_files,
        video_clicks=None,
        ad_parameters=None,
        tracking_events=parse_tracking_creatives(tracking_events),
    )


@accept_none
def parse_tracking_creatives(xml_dict):
    tracking_events = xml_dict["Tracking"]
    # There is only one
    if isinstance(tracking_events, dict):
        return [parse_tracking_event(tracking_events)]

    # There are several
    if isinstance(tracking_events, list):
        return [parse_tracking_event(t) for t in tracking_events]

    return None


def parse_tracking_event(xml_dict):
    required_fields = ("@event", "#text")
    event, uri = extract_fields(xml_dict, required_fields)
    return v2_models.make_tracking_event(uri, event)


@accept_none
def parse_media_files(xml_dict):
    media_files = xml_dict["MediaFile"]
    # There is only one media file
    if isinstance(media_files, dict):
        return [parse_media_file(media_files)]

    # There are several media files
    if isinstance(media_files, list):
        return [parse_media_file(m) for m in media_files]

    return None


def parse_media_file(xml_dict):
    required_fields = ["#text", "@delivery", "@type", "@width", "@height"]
    asset, delivery, type, width, height = extract_fields(xml_dict, required_fields)

    maybe_required_fields = ("@bitrate", "@minBitrate", "@maxBitrate")
    bitrate, min_bitrate, max_bitrate = extract_fields(xml_dict, maybe_required_fields, method="optional")

    no_bitrate_types = (u'application/x-shockwave-flash', u"application/javascript")
    if delivery == "progressive" and type not in no_bitrate_types and bitrate is None:
        msg = "Bitrate must be declared when delivery is progressive in {xml_dict}"
        raise ParseError(msg.format(xml_dict=xml_dict))
    if delivery == "streaming" and  type not in no_bitrate_types and (min_bitrate is None or max_bitrate is None):
        msg = "Min and Max Bitrate must be declared when delivery is streaming in {xml_dict}"
        raise ParseError(msg.format(xml_dict=xml_dict))

    optional_fields = ("@scalable", "@maintainAspectRatio", "@apiFramework")
    scalable, maintain_aspect_ratio, api_framework = extract_fields(xml_dict, optional_fields, method="optional")
    if scalable is not None:
        scalable = to_bool(scalable)
    if maintain_aspect_ratio is not None:
        maintain_aspect_ratio = to_bool(maintain_aspect_ratio)

    return v2_models.make_media_file(
        asset=asset,
        delivery=delivery,
        type=type,
        width=width,
        height=height,
        bitrate=bitrate,
        min_bitrate=min_bitrate,
        max_bitrate=max_bitrate,
        scalable=scalable,
        maintain_aspect_ratio=maintain_aspect_ratio,
        api_framework=api_framework,
    )
