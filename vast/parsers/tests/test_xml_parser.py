from unittest import TestCase


from vast.parsers import xml_parser
from vast.models import vast_v2 as v2_models
from vast import resources


class TestWrapperParser(TestCase):
    def test_simple_wrapper_parsed(self):
        with open(resources.SIMPLE_WRAPPER_XML, "r") as fp:
            xml_string = fp.read()

        actual = xml_parser.from_xml_string(xml_string)
        expected = v2_models.Vast.make(
            version=u"2.0",
            ad=v2_models.Ad.make_wrapper(
                id=u"70470",
                wrapper=v2_models.Wrapper.make(
                    ad_system=u"MagU",
                    vast_ad_tag_uri=u"//vast.dv.com/v3/vast?_vast",
                    ad_title=None,
                    impression=u"//magu.d.com/vidimp",
                    error=u"//magu.d.com/viderr?err=[ERRORCODE]",
                    creatives=None,
                ),
            ),
        )
        self.assertEqual(actual, expected)


class TestInlineParser(TestCase):
    def test_simple_inline_parsed(self):
        with open(resources.SIMPLE_INLINE_XML, "r") as fp:
            xml_string = fp.read()

        actual = xml_parser.from_xml_string(xml_string)
        expected = v2_models.Vast.make(
            version=u"2.0",
            ad=v2_models.Ad.make_inline(
                id=u"509080ATOU",
                inline=v2_models.Inline.make(
                    ad_system=u"MagU",
                    ad_title=u"Centers for Disease Control and Prevention: Who Needs a Flu Vaccine",
                    impression=u"https://mag.dom.com/admy?ad_id=509080ATOU",
                    creatives=[
                        v2_models.Creative.make(
                            linear=v2_models.LinearCreative.make(
                                duration=15,
                                media_files=[
                                    v2_models.MediaFile.make(
                                        asset=u"https://www.cdc.gov/flu/video/who-needs-flu-vaccine-15_720px.mp4",
                                        delivery=u"progressive",
                                        type=u"video/mp4",
                                        bitrate=300,
                                        width=720,
                                        height=420,
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            ),
        )
        self.assertEqual(actual, expected)

    def test_inline_multi_media_files_parsed(self):
        with open(resources.INLINE_MULTI_FILES_XML, "r") as fp:
            xml_string = fp.read()

        actual = xml_parser.from_xml_string(xml_string)
        expected = v2_models.Vast.make(
            version=u"2.0",
            ad=v2_models.Ad.make_inline(
                id=u"509080ATOU",
                inline=v2_models.Inline.make(
                    ad_system=u"MagU",
                    ad_title=u"Many Media Files",
                    impression=u"https://mag.dom.com/admy?ad_id=509080ATOU",
                    creatives=[
                        v2_models.Creative.make(
                            linear=v2_models.LinearCreative.make(
                                duration=15,
                                media_files=[
                                    v2_models.MediaFile.make(
                                        asset=u"https://vpaid.dv.com/s.swf",
                                        delivery=u"progressive",
                                        type=u"application/x-shockwave-flash",
                                        width=176,
                                        height=144,
                                        api_framework=u"VPAID",
                                    ),
                                    v2_models.MediaFile.make(
                                        asset=u"https://vpaid.dv.com/js/vpaid-wrapper-dv.js",
                                        delivery=u"progressive",
                                        type=u"application/javascript",
                                        width=176,
                                        height=144,
                                        api_framework=u"VPAID",
                                    ),
                                    v2_models.MediaFile.make(
                                        asset=u"https://dv.2mdn.net/videoplayback/id/f5316658i7/file.3gpp",
                                        delivery=u"streaming",
                                        type=u"video/3gpp",
                                        width=176,
                                        height=144,
                                        min_bitrate=51,
                                        max_bitrate=900,
                                        scalable=False,
                                        maintain_aspect_ratio=False,
                                    ),
                                    v2_models.MediaFile.make(
                                        asset=u"https://dv.2mdn.net/videoplayback/f5316658i78776/file.3gpp",
                                        delivery=u"progressive",
                                        type=u"video/3gpp",
                                        width=320,
                                        height=180,
                                        bitrate=177,
                                        scalable=False,
                                        maintain_aspect_ratio=False,
                                    ),
                                    v2_models.MediaFile.make(
                                        asset=u"https://dv.2mdn.net/videoplayback/id/f5316658cd737d42/file/file.mp4",
                                        delivery=u"progressive",
                                        type=u"video/mp4",
                                        width=640,
                                        height=360,
                                        bitrate=409,
                                        scalable=False,
                                        maintain_aspect_ratio=False,
                                    ),
                                    v2_models.MediaFile.make(
                                        asset=u"https://dv.2mdn.net/videoplayback/id/f5316658cd737d42/file.webm",
                                        delivery=u"progressive",
                                        type=u"video/webm",
                                        bitrate=2452,
                                        width=1280,
                                        height=720,
                                        scalable=False,
                                        maintain_aspect_ratio=False,
                                    ),
                                    v2_models.MediaFile.make(
                                        asset=u"https://dv.2mdn.net/index.m3u8",
                                        delivery=u"progressive",
                                        type=u"application/x-mpegURL",
                                        bitrate=105,
                                        width=256,
                                        height=144,
                                        scalable=False,
                                        maintain_aspect_ratio=False,
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            ),
        )
        self.assertEqual(actual, expected)


class TestInlineWithTrackingEvents(TestCase):
    def test_xml_with_tracking(self):
        with open(resources.INLINE_WITH_TRACKING_EVENTS_XML, "r") as fp:
            xml_string = fp.read()

        actual = xml_parser.from_xml_string(xml_string)
        expected = v2_models.Vast.make(
            version=u"2.0",
            ad=v2_models.Ad.make_inline(
                id=u"509080ATOU",
                inline=v2_models.Inline.make(
                    ad_system=u"MagU",
                    ad_title=u"Inline with Tracking Events",
                    impression=u"https://mag.dom.com/admy?ad_id=509080ATOU",
                    creatives=[
                        v2_models.Creative.make(
                            linear=v2_models.LinearCreative.make(
                                duration=15,
                                media_files=[
                                    v2_models.MediaFile.make(
                                        asset=u"https://www.cdc.gov/flu/video/who-needs-flu-vaccine-15_720px.mp4",
                                        delivery=u"progressive",
                                        type=u"video/mp4",
                                        width=720,
                                        height=420,
                                        bitrate=300,
                                    ),
                                ],
                                tracking_events=[
                                    v2_models.TrackingEvent.make(
                                        tracking_event_uri=u'https://mag.dom.com/vidtrk?evt=creativeView',
                                        tracking_event_type=u"creativeView"
                                    ),
                                    v2_models.TrackingEvent.make(
                                        tracking_event_uri=u'https://mag.dom.com/vidtrk?evt=start',
                                        tracking_event_type=u"start"
                                    ),
                                    v2_models.TrackingEvent.make(
                                        tracking_event_uri=u'https://mag.dom.com/vidtrk?evt=midpoint',
                                        tracking_event_type=u"midpoint"
                                    ),
                                    v2_models.TrackingEvent.make(
                                        tracking_event_uri=u'https://mag.dom.com/vidtrk?evt=firstQuartile',
                                        tracking_event_type=u"firstQuartile"
                                    ),
                                    v2_models.TrackingEvent.make(
                                        tracking_event_uri=u'https://mag.dom.com/vidtrk?evt=thirdQuartile',
                                        tracking_event_type=u"thirdQuartile"
                                    ),
                                    v2_models.TrackingEvent.make(
                                        tracking_event_uri=u'https://mag.dom.com/vidtrk?evt=complete',
                                        tracking_event_type=u"complete"
                                    ),
                                    v2_models.TrackingEvent.make(
                                        tracking_event_uri=u'https://mag.dom.com/vidtrk?evt=mute',
                                        tracking_event_type=u"mute"
                                    ),
                                    v2_models.TrackingEvent.make(
                                        tracking_event_uri=u'https://mag.dom.com/vidtrk?evt=unmute',
                                        tracking_event_type=u"unmute"
                                    ),
                                    v2_models.TrackingEvent.make(
                                        tracking_event_uri=u'https://mag.dom.com/vidtrk?evt=rewind',
                                        tracking_event_type=u"rewind"
                                    ),
                                    v2_models.TrackingEvent.make(
                                        tracking_event_uri=u'https://mag.dom.com/vidtrk?evt=resume',
                                        tracking_event_type=u"resume"
                                    ),
                                    v2_models.TrackingEvent.make(
                                        tracking_event_uri=u'https://mag.dom.com/vidtrk?evt=fullscreen',
                                        tracking_event_type=u"fullscreen"
                                    ),
                                    v2_models.TrackingEvent.make(
                                        tracking_event_uri=u'https://mag.dom.com/vidtrk?evt=collapse',
                                        tracking_event_type=u"collapse"
                                    ),
                                    v2_models.TrackingEvent.make(
                                        tracking_event_uri=u'https://mag.dom.com/vidtrk?evt=acceptInvitation',
                                        tracking_event_type=u"acceptInvitation"
                                    ),
                                    v2_models.TrackingEvent.make(
                                        tracking_event_uri=u'https://mag.dom.com/vidtrk?evt=close',
                                        tracking_event_type=u"close"
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            ),
        )
        self.assertEqual(actual, expected)

    def test_xml_with_creative_attributes(self):
        with open(resources.INLINE_WITH_CREATIVE_ATTRIBUTES, "r") as fp:
            xml_string = fp.read()

        actual = xml_parser.from_xml_string(xml_string)

        expected = v2_models.Vast.make(
            version=u"2.0",
            ad=v2_models.Ad.make_inline(
                id=u"509080ATOU",
                inline=v2_models.Inline.make(
                    ad_system=u"MagU",
                    ad_title=u"Centers for Disease Control and Prevention: Who Needs a Flu Vaccine",
                    impression=u"https://mag.dom.com/admy?ad_id=509080ATOU",
                    creatives=[
                        v2_models.Creative.make(
                            linear=v2_models.LinearCreative.make(
                                duration=15,
                                media_files=[
                                    v2_models.MediaFile.make(
                                        asset=u"https://www.cdc.gov/flu/video/who-needs-flu-vaccine-15_720px.mp4",
                                        delivery=u"progressive",
                                        type=u"video/mp4",
                                        bitrate=300,
                                        width=720,
                                        height=420,
                                    ),
                                ],
                            ),
                            id=81997481,
                            sequence=1,
                            ad_id=u"MagU",
                            api_framework=v2_models.ApiFramework.VPAID,
                        ),
                    ],
                ),
            ),
        )
        self.assertEqual(actual, expected)

    def test_xml_with_video_clicks(self):
        with open(resources.INLINE_WITH_VIDEO_CLICKS, "r") as fp:
            xml_string = fp.read()

        actual = xml_parser.from_xml_string(xml_string)

        expected = v2_models.Vast.make(
            version=u"2.0",
            ad=v2_models.Ad.make_inline(
                id=u"509080ATOU",
                inline=v2_models.Inline.make(
                    ad_system=u"MagU",
                    ad_title=u"Centers for Disease Control and Prevention: Who Needs a Flu Vaccine",
                    impression=u"https://mag.dom.com/admy?ad_id=509080ATOU",
                    creatives=[
                        v2_models.Creative.make(
                            linear=v2_models.LinearCreative.make(
                                duration=15,
                                media_files=[
                                    v2_models.MediaFile.make(
                                        asset=u"https://www.cdc.gov/flu/video/who-needs-flu-vaccine-15_720px.mp4",
                                        delivery=u"progressive",
                                        type=u"video/mp4",
                                        bitrate=300,
                                        width=720,
                                        height=420,
                                    ),
                                ],
                                video_clicks=v2_models.VideoClicks.make(
                                    click_through=u"https://mag.dom.com/click_through",
                                    click_tracking=u"https://mag.dom.com/click_tracking",
                                    custom_click=u"https://mag.dom.com/custom_click"
                                )
                            ),
                        ),
                    ],
                ),
            ),
        )
        self.assertEqual(actual, expected)

    def test_xml_ad_attributes(self):
        with open(resources.INLINE_WITH_AD_PARAMETERS, "r") as fp:
            xml_string = fp.read()

        actual = xml_parser.from_xml_string(xml_string)

        expected = v2_models.Vast.make(
            version=u"2.0",
            ad=v2_models.Ad.make_inline(
                id=u"509080ATOU",
                inline=v2_models.Inline.make(
                    ad_system=u"MagU",
                    ad_title=u"Centers for Disease Control and Prevention: Who Needs a Flu Vaccine",
                    impression=u"https://mag.dom.com/admy?ad_id=509080ATOU",
                    creatives=[
                        v2_models.Creative.make(
                            linear=v2_models.LinearCreative.make(
                                duration=15,
                                media_files=[
                                    v2_models.MediaFile.make(
                                        asset=u"https://www.cdc.gov/flu/video/who-needs-flu-vaccine-15_720px.mp4",
                                        delivery=u"progressive",
                                        type=u"video/mp4",
                                        bitrate=300,
                                        width=720,
                                        height=420,
                                    ),
                                ],
                                ad_parameters=v2_models.AdParameters.make(
                                    data=u"{data : funky data goes here}",
                                    xml_encoded=False,
                                )
                            ),
                        ),
                    ],
                ),
            ),
        )
        self.assertEqual(actual, expected)
