from setuptools import setup, find_packages

version = '1.4'

setup(name='collective.confirmableforms',
      version=version,
      description="A Plone add on to simplify form confirmation by e-mail.",
      long_description=(open("README.txt").read() + "\n" +
                        open("CHANGES.rst").read()),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
          "Framework :: Plone",
          "Programming Language :: Python",
          ],
      keywords='',
      author='Vincent Pretre',
      author_email='v.pretre@zestsoftware.nl',
      url='https://github.com/zestsoftware/collective.confirmableforms',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'Products.PloneFormGen',
          'collective.depositbox',
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
