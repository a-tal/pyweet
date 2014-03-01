"""Pyweet's basic setup.py config."""


from distutils.core import setup
from src import __version__


setup(
    name="pyweet",
    version=__version__,
    author="Adam Talsma",
    author_email="adam@talsma.ca",
    package_dir={"pyweet": "src"},
    packages=["pyweet"],
    requires=["twitter"],
    scripts=["bin/pyweet"],
    url="https://github.com/a-tal/pyweet",
    description="Twitter command line util",
    long_description="Yet another Twitter command line utility.",
    download_url="https://github.com/a-tal/pyweet",
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
