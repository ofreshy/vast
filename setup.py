import sys

from setuptools import find_packages, setup


if sys.version_info[:2] < (2, 7):
    raise Exception("Vast lib only work on Python 2.7 ang greater or PyPy")



setup(
    name="vast",
    description="Utility to parse vast XML documents",
    url="https://github.com/ofreshy/vast",
    author="Offer Sharabi",
    author_email="sharoffer@gmail.com",
    packages=find_packages(),
    install_requires=[],
    setup_requires=["vcversioner"],
    vcversioner={"version_module_paths": ["vast/_version.py"]},
)
