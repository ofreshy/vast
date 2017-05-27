from unittest import TestCase


from vast.parsers import xml_parser
from vast.models import vast_v2 as v2_models
from vast.models.vast_v2 import Ad, Creative, LinearCreative, Vast, Wrapper
from vast.resources import SIMPLE_INLINE_XML, SIMPLE_WRAPPER_XML


class TestWrapperParser(TestCase):
    def test_simple_wrapper_parsed(self):
        with open(SIMPLE_WRAPPER_XML, "r") as fp:
            xml_string = fp.read()

        actual = xml_parser.from_xml_string(xml_string)
        expected = Vast.make(
            version=u"2.0",
            ad=Ad.make(
                id=u"70470",
                wrapper=Wrapper.make(
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
    def test_simple_wrapper_parsed(self):
        with open(SIMPLE_INLINE_XML, "r") as fp:
            xml_string = fp.read()

        actual = xml_parser.from_xml_string(xml_string)
        expected = Vast.make(
            version=u"2.0",
            ad=Ad.make(
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


