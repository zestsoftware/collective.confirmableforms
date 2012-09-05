from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.depositbox.store import Box
from Products.Archetypes.interfaces.field import IField
from Products.PloneFormGen import implementedOrProvidedBy

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
                  if not implementedOrProvidedBy(IField, fo)]

        self.request.form = data
        self.context.send_form(fields, self.request)

        thanks = form.get(form.thanksPage)
        return thanks()
