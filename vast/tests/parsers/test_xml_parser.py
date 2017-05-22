from unittest import TestCase


from vast.parsers import xml_parser
from vast.models.vast_v2 import Vast, Ad, Wrapper
from vast.resources import SIMPLE_WRAPPER_XML


class TestWrapperParser(TestCase):
    def setUp(self):
        pass

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
