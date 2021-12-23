from collective.confirmableforms.interfaces import IConfirmedSubmission
from Products.Archetypes.interfaces.field import IField
from Products.Five import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from zope.interface import alsoProvides

import transaction

try:
    from plone.protect.interfaces import IDisableCSRFProtection
except ImportError:
    IDisableCSRFProtection = None


class ConfirmedFormView(BrowserView):
    def __call__(self):
        box = self.context.get_box()
        secret = self.request.form.get("secret")
        email = self.request.form.get("email")
        data = box.pop(secret, token=email)
        if IDisableCSRFProtection:
            # We may have changed data, and this is usually a GET request,
            # so we should avoid a CSRF warning.
            alsoProvides(self.request, IDisableCSRFProtection)

        if data is None:
            return self.index()

        alsoProvides(self.request, IConfirmedSubmission)
        form = self.context.get_form()
        fields = [fo for fo in form._getFieldObjects() if not IField.providedBy(fo)]

        # Put the data in the request.  Make it a dictionary,
        # otherwise the fg_result_view does not work, as an anonymous
        # user is not authorized to get items from the data, as it is
        # a PersistentMapping.
        self.request.form = dict(data)

        # Send mail that would be send when this would have been
        # a standard FormMailerAdapter.
        if self.context.send_standard_mail:
            self.context.send_form(fields, self.request)

        # Process the other adapters.  First argument is 'errors'.
        result = form.fgProcessActionAdapters({}, fields=fields, REQUEST=self.request)
        if result:
            # We have an error.  Abort any changes.
            transaction.abort()
            IStatusMessage(self.request).addStatusMessage(result, type="error")
            return self.index()

        # Get the thank you page.
        thankspage = self.context.thanksPage
        if not thankspage:
            thankspage = form.thanksPage
        thanks = form.get(thankspage)
        if thanks is None:
            thanks = form.unrestrictedTraverse("fg_result_view")
        return thanks()
