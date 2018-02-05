from Products.PloneFormGen.interfaces import IPloneFormGenActionAdapter
from zope.interface import Interface


class IConfirmedFormMailerAdapter(IPloneFormGenActionAdapter):
    """Our confirmed version of the standard PFG mailer action adapter."""


class IInitialSubmission(Interface):
    """Marker interface for request when a PFG form is initially submitted."""


class IConfirmedSubmission(Interface):
    """Marker interface for request when a mail is successfully confirmed."""
