Changelog
=========

2.1.2 (2021-12-24)
------------------

- Avoid CSRF warning when confirming.  [maurits]

- Put email address without brackets as token in the box.
  [maurits]


2.1.1 (2019-08-19)
------------------

- Updated Dutch translations.  [maurits]


2.1.0 (2019-08-19)
------------------

- Added fields for setting the confirmation email address.
  As fallback, use the standard recipent email address.
  Until now, we only used the address of the ``replyto`` field.
  [maurits]

- Pass ``wrappedFields`` option to the confirm mailer templates.
  Same as PloneFormGen does for the standard mailer.  [maurits]


2.0.0 (2018-02-05)
------------------

- Added ``send_standard_mail`` boolean.  Default is true.
  If set, after the email address is confirmed, the standard mail is sent,
  as if this was a standard mail action adapter.
  [maurits]

- Automatically ignore all other action adapters during first submission.
  Automatically ignore our ConfirmedFormMailerAdapter after confirmed submission.
  This makes it possible to have for example a Script adapter called only after confirmed submission.
  [maurits]

- Automatically install PloneFormGen during our own install.
  This makes sure PloneFormGen is installed first.
  [maurits]


1.4.3 (2016-11-18)
------------------

- Added more info in readme on how to use this.  [maurits]

- Package cleanup. Added test extra, although we have no interesting tests.
  [maurits]


1.4.2 (2013-05-31)
------------------

- Do not give our ConfirmedFormMailerAdapter a workflow.
  [maurits]

- Make more secure.
  [maurits]


1.4.1 (2013-05-06)
------------------

- Remove implementedOrProvidedBy import from PloneFormGen that was only meant
  for Z2 interfaces compatibility. Removed from PFG 1.7.7.
  [fredvd]


1.4 (2012-09-14)
----------------

- Make the plain_mail and html_mail fields optional, but give a
  validation error when neither of them is filled in.
  [maurits]

- Add a field to select a different thank-you page to show when the
  form has been confirmed.  Fall back to the standard thank-you page
  of the form or the fg_result_view page.
  [maurits]

- When there is no plain text or no html text, do not send that part.
  [maurits]

- Do not use a RichTextWidget for the html field.  Any tal tags
  would get stripped.
  [maurits]


1.3.1 (2012-09-11)
------------------

- Translate the Confirmation schemata tab.
  [maurits]


1.3 (2012-09-11)
----------------

- Time during which the form can be confirmed is now a setting in the
  confirmer. [vincent]


1.2.1 (2012-09-07)
------------------

- Fixes with schemata that was causing error when saving our custom CT
  objects. [vincent]


1.2 (2012-09-07)
----------------

- Sender email is not mandatory anymore. We use the one set in Plone
  if no address is given. [vincent]

- Dutch translations. [jladage]

- Fixes in labels and display in the edit form. [vincent]


1.1 (2012-09-07)
----------------

- Nothing changed yet.


1.0 (2012-09-06)
----------------

- Initial release
