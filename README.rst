Introduction
============

This product adds a new emailer for Products.PloneFormGen. Our emailer
is based on the default PFG one, but will first send an email to the
person who submitted the form so he can confirm his email address.

This products relies on PloneFormGen and collective.depositbox to
store the data waiting for validation.


Compatibility
=============

This has been tested with Plone 4.3 and PloneFormGen 1.7.


Installing
==========

Add ``collective.confirmableforms`` to your buildout and install it
via Zope quick installer or Plone add-on control panel page.  First
install ``PloneFormGen`` itself, then ``collective.confirmableforms``.


Form setup
==========

- Add a PloneFormGen form.

- In this form, add a Confirmed Mailer Adapter.

- On the Confirmation tab of this mailer, set a plain or html text
  that includes ``[[confirmation_link]]`` to display the confirmation
  link.

- Remove any other action adapters from the form, especially the
  default Mailer Adapter, otherwise the other actions are executed
  anyway, even when the form has not been confirmed via email yet.

- You probably want to edit the thanks page and say here that the user
  will be getting an email and should click on the link there.

- You can add a second thanks page to say that the email has been succesfully confirmed.
  Edit the Confirmed Mailer Adapter and select this as thanks page on the confirmation tab.


How it works for the visitor
============================

- A visitor fills in the form and submits it.

- The thanks page of the form is displayed.

- The visitor gets an email with a link to confirm his input.

- The visitor clicks on the link.

- The normal part of the mailer kicks in, sending an email to an admin, or however you have set it up.
  This works the same as the default mailer.

- The visitor sees the thanks page that is configured in the Confirmed Mailer Adapter.


Sponsorship
===========

Work on collective.confirmableforms has been made possible by The Flemish
Environment Agency or VMM. See http://www.vmm.be. VMM operates as an agency of
the Flemish government for a better environment in Flanders. Flanders is one of
the three Belgian regions with its own government, parliament and
administration. The other two are the Brussels-Capital Region and the Walloon
Region.


Links
=====

- Code: https://github.com/zestsoftware/collective.confirmableforms

- Issue tracker: https://github.com/zestsoftware/collective.confirmableforms/issues
