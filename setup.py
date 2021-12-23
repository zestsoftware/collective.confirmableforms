from setuptools import setup, find_packages

version = "2.1.2"

setup(
    name="collective.confirmableforms",
    version=version,
    description="A Plone add on to simplify form confirmation by e-mail.",
    long_description=(open("README.rst").read() + "\n" + open("CHANGES.rst").read()),
    # Get more strings from https://pypi.org/classifiers
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ],
    keywords="PloneFormGen confirmation email",
    author="Vincent Pretre",
    author_email="v.pretre@zestsoftware.nl",
    url="https://github.com/zestsoftware/collective.confirmableforms",
    license="GPL",
    packages=find_packages(exclude=["ez_setup"]),
    namespace_packages=["collective"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "setuptools",
        "Products.PloneFormGen",
        "collective.depositbox",
        "collective.monkeypatcher",
    ],
    extras_require={
        "test": [
            "Products.PloneTestCase",
        ],
    },
    entry_points="""
    # -*- Entry points: -*-

    [z3c.autoinclude.plugin]
    target = plone
    """,
)
