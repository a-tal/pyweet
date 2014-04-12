"""Pyweet's setup/installer."""


from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    """Shim in pytest to be able to use it with setup.py test."""

    def finalize_options(self):
        """Stolen from http://pytest.org/latest/goodpractises.html."""

        TestCommand.finalize_options(self)
        self.test_args = ["-v", "-rf", "--cov", "pyweet", "test"]
        self.test_suite = True

    def run_tests(self):
        """Also shamelessly stolen."""

        # have to import here, outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        raise SystemExit(errno)


setup(
    name="pyweet",
    version="0.0.5",
    author="Adam Talsma",
    author_email="adam@talsma.ca",
    packages=["pyweet"],
    install_requires=["twitter"],
    scripts=["bin/pyweet"],
    url="https://github.com/a-tal/pyweet",
    description="Twitter command line util",
    long_description="Yet another Twitter command line utility.",
    download_url="https://github.com/a-tal/pyweet",
    tests_require=["pytest", "mock", "pytest-cov", "coverage"],
    cmdclass={"test": PyTest},
    license="BSD",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
    ],
)
