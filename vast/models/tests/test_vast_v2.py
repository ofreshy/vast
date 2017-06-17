import unittest

from vast.models import vast_v2
from vast.models.tests.vast_v2_model_mixin import VastModelMixin


class TestAsDict(unittest.TestCase):
    def test_linear(self):
        linear = vast_v2.LinearCreative.make(
            duration=15,
            media_files=(
                vast_v2.make_media_file(
                    asset=u"https://www.dom.com",
                    delivery=u"progressive",
                    type=u"video/mp4",
                    width=1,
                    height=1,
                    bitrate=300,
                ),
            ),
        )
        print linear.as_dict()



class TestMakeVast(VastModelMixin, unittest.TestCase):
    def test_valid_passes(self):
        try:
            vast_v2.Vast.make(
                version="2.0",
                ad=self.make_wrapper_ad(),
            )
        except Exception as e:
            self.fail("Failed to make vast,  %s" % e)


class TestMakeTrackingEvent(VastModelMixin, unittest.TestCase):
    def test_valid_tracking_event_passes(self):
        try:
            self.make_tracking_event()
        except ValueError as e:
            self.fail("Failed to make tracking_event, %s" % e)


