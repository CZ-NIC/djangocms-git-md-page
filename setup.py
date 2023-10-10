# /usr/bin/python3
"""Setup script for djangocms-git-md-page."""
from distutils.command.build import build

from setuptools import find_packages, setup


class CustomBuild(build):
    sub_commands = [("compile_catalog", lambda x: True)] + build.sub_commands


setup(
    packages=find_packages(exclude=["*.tests"]),
    cmdclass={"build": CustomBuild},
    setup_requires=["Babel >=2.3"],
    include_package_data=True,
)
