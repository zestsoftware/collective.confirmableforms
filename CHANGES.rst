Changelog
=========

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
