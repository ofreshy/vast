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


class TestInValidatorWhenIn(TestWithScenarios):
    scenarios = [
        ("in_tuple",
         dict(name="in_tuple", collection=("a", "b"), value="a")),
        ("in_list",
         dict(name="in_list", collection=["a", "b"], value="a")),
        ("in_set",
         dict(name="in_set", collection={"a", "b"}, value="a")),
        ("in_dict",
         dict(name="in_dict", collection={"a":1, "b":2}, value="a")),
    ]

    def test_in_validator(self):
        in_validator = validators.make_in_validator(self.collection)
        try:
            in_validator(self.value, self.name)
        except ValueError:
            self.fail("%s in validator failed" % self.name)


class TestInValidatorWhenOut(TestWithScenarios):
    scenarios = [
        ("not_in_tuple",
         dict(name="not_in_tuple", collection=("a", "b"), value="c")),
        ("not_in_list",
         dict(name="not_in_list", collection=["a", "b"], value="c")),
        ("not_in_set",
         dict(name="not_in_set", collection={"a", "b"}, value="c")),
        ("not_in_dict",
         dict(name="not_in_dict", collection={"a": 1, "b": 2}, value="c")),
    ]

    def test_in_validator(self):
        in_validator = validators.make_in_validator(self.collection)
        with self.assertRaises(ValueError):
            in_validator(self.value, self.name)
