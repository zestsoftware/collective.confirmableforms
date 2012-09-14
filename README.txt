Introduction
============

This product adds a new emailer for Products.PloneFormGen. Our emailer
is based on the default PFG one, but will first send an email to the
person who submitted the form so he can confirm his email address.

This products relies on PloneFormGen and collective.depositbox to
store the data waiting for validation.


Installing
==========

Add ``collective.confirmableforms`` to your buildout and install it
via Zope quick installer or Plone add-on control panel page.  First
install ``PloneFormGen`` itself, then ``collective.confirmableforms``.
