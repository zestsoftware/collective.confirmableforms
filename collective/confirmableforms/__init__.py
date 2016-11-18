from Products.Archetypes import listTypes
from Products.Archetypes.atapi import process_types
from Products.CMFCore import utils as cmfutils
from zope.i18nmessageid import MessageFactory

import config


ConfirmableFormsMessageFactory = MessageFactory(config.PROJECTNAME)


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
    import content  # noqa

    permissions = dict(
        ConfirmedFormMailerAdapter=(
            'confirmableforms: add Confirmed Form Mailer Adapter'),
    )

    # Initialize portal content
    content_types, constructors, ftis = process_types(
        listTypes(config.PROJECTNAME),
        config.PROJECTNAME)

    allTypes = zip(content_types, constructors)
    for atype, constructor in allTypes:
        kind = "%s: %s" % (config.PROJECTNAME, atype.archetype_name)
        cmfutils.ContentInit(
            kind,
            content_types=(atype, ),
            permission=permissions[atype.portal_type],
            extra_constructors=(constructor, ),
        ).initialize(context)
