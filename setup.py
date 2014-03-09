"""Pyweet's setup/installer."""


from setuptools import setup


setup(
    name="pyweet",
    version="0.0.4",
    author="Adam Talsma",
    author_email="adam@talsma.ca",
    package_dir={"pyweet": "src"},
    packages=["pyweet"],
    install_requires=["twitter"],
    scripts=["bin/pyweet"],
    url="https://github.com/a-tal/pyweet",
    description="Twitter command line util",
    long_description="Yet another Twitter command line utility.",
    download_url="https://github.com/a-tal/pyweet",
    tests_require=['nose'],
    test_suite='nose.collector',
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
