import unittest

from testscenarios import TestWithScenarios

from vast.models import vast_v2
from vast.models.tests.vast_v2_model_mixin import VastModelMixin


class TestAsDict(unittest.TestCase):
    def test_linear(self):
        linear = vast_v2.LinearCreative.make(
            duration=15,
            media_files=(
                vast_v2.MediaFile.make(
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


class TestVastMixinDefaultsWork(VastModelMixin, TestWithScenarios):
    scenarios = [
        ("make_vast", dict(make_func="make_vast")),
        ("make_wrapper_ad", dict(make_func="make_wrapper_ad")),
        ("make_inline_ad", dict(make_func="make_inline_ad")),
        ("make_wrapper", dict(make_func="make_wrapper")),
        ("make_inline", dict(make_func="make_inline")),
        ("make_creatives", dict(make_func="make_creatives")),
        ("make_creative", dict(make_func="make_creative")),
        ("make_linear_creative", dict(make_func="make_linear_creative")),
        ("make_media_files", dict(make_func="make_media_files")),
        ("make_media_file", dict(make_func="make_media_file")),
        ("make_tracking_event", dict(make_func="make_tracking_event")),
    ]

    def test_it_makes_it(self):
        try:
            getattr(self, self.make_func)()
        except Exception as e:
            self.fail("make func failed,  %s" % e)

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


class TestLinearCreative(VastModelMixin, unittest.TestCase):
    def test_valid_linear_creative(self):
        try:
            self.make_linear_creative()
        except ValueError as e:
            self.fail("Failed to make tracking_event, %s" % e)
