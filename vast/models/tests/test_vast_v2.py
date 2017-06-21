from testscenarios import TestWithScenarios

from vast.errors import IllegalModelStateError
from vast.models import vast_v2
from vast.models.tests.vast_v2_model_mixin import VastModelMixin


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


class TestVastIllegals(VastModelMixin, TestWithScenarios):
    scenarios = [
        ("version mismatch", dict(update=dict(version=3.0))),
        ("ad is None", dict(update=dict(ad=None)))
    ]

    def test_it_breaks(self):
        kw = dict(version=u"2.0", ad=self.make_wrapper_ad())
        kw.update(self.update)
        with self.assertRaises(IllegalModelStateError):
            # We call the model directly here,
            # since we want to test the model make method,
            # not our mixin
            vast_v2.Vast.make(**kw)
