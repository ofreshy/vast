import unittest

from vast.models import vast_v2


class TestAsDict(unittest.TestCase):
    def test_linear(self):
        linear = vast_v2.make_linear_creative(
            duration=15,
            media_files=(
                vast_v2.make_media_file(
                    asset=u"https://www.dom.com",
                    delivery=u"progressive",
                    type=u"video/mp4",
                    width=1,
                    height=1,
                    bitrate=300,
                )
            )
        )
        print linear.as_dict()