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
            ad=v2_models.Ad.make(
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
            ad=v2_models.Ad.make(
                id=u"509080ATOU",
                inline=v2_models.InLine.make(
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
            ad=v2_models.Ad.make(
                id=u"509080ATOU",
                inline=v2_models.InLine.make(
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
