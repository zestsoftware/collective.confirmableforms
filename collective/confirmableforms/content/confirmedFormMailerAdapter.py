from Products.Archetypes import atapi
from AccessControl import ClassSecurityInfo

from Products.PloneFormGen.content.formMailerAdapter import FormMailerAdapter, formMailerAdapterSchema

from collective.confirmableforms import config

confirmedFormMailerAdapterSchema = formMailerAdapterSchema.copy()

class ConfirmedFormMailerAdapter(FormMailerAdapter):
    schema = confirmedFormMailerAdapterSchema
    security = ClassSecurityInfo()

    security.declarePrivate('onSuccess')
    def onSuccess(self, fields, REQUEST=None):
        # Well, we'll deal with that later on.
        pass

atapi.registerType(ConfirmedFormMailerAdapter, config.PROJECTNAME)
