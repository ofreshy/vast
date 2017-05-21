from testscenarios import TestWithScenarios

from vast.models import vast_v2
from vast import validators


class TestValidTypeValidator(TestWithScenarios):
    scenarios = [
        ("str", dict(type=str, value="str")),
        ("int", dict(type=int, value=5)),
        ("other class", dict(
            type=vast_v2.MediaFile,
            value=vast_v2.MediaFile.make(
                "streaming", "g", 0, 9, min_bitrate=10, max_bitrate=100,
            ))
         )
    ]

    def test_it_passes(self):
        try:
            v = validators.make_type_validator(self.type)
            v(self.value, str(self.type))
        except TypeError:
            self.fail("validation failed for type %s" % self.type)


class TestInvalidTypeValidator(TestWithScenarios):
    scenarios = [
        ("str", dict(type=str, value=5)),
        ("int", dict(type=int, value="5")),
        ("other class", dict(type=vast_v2.MediaFile, value=5.6)),
    ]

    def test_it_fails(self):
        with self.assertRaises(TypeError):
            v = validators.make_type_validator(self.type)
            v(self.value, str(self.type))


# TODO TBD
