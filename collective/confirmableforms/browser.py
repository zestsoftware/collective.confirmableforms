from Products.Archetypes.interfaces.field import IField
from Products.Five import BrowserView


class ConfirmedFormView(BrowserView):

    def __call__(self):
        box = self.context.get_box()
        secret = self.request.form.get('secret')
        email = self.request.form.get('email')
        data = box.pop(secret, token=email)

        if data is None:
            return self.index()

        form = self.context.get_form()
        fields = [fo for fo in form._getFieldObjects()
                  if not IField.providedBy(fo)]

        # Put the data in the request.  Make it a dictionary,
        # otherwise the fg_result_view does not work, as an anonymous
        # user is not authorized to get items from the data, as it is
        # a PersistentMapping.
        self.request.form = dict(data)
        self.context.send_form(fields, self.request)

        # Get the thank you page.
        thankspage = self.context.thanksPage
        if not thankspage:
            thankspage = form.thanksPage
        thanks = form.get(thankspage)
        if thanks is None:
            thanks = form.unrestrictedTraverse('fg_result_view')
        return thanks()
