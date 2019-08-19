"""Patch PloneFormGen.

On initial form submission, we do not want any action adapters to run.
Only our own ConfirmedFormMailerAdapter must run.
This sends an email with a confirmation link.
The confirmation link is handled by a browser view.
This view does some checks, and runs all action adapters, except itself.
That is the goal of the patches in this file.

First, we patch getRawActionAdapter and let it return what we want.
Problem: this method is also called when a Manager edits the form.

Q: So how do we know if this is a form submission or an edit by a Manager?
A: We know it is a form submission when fgProcessActionAdapters is called.

Q: How do we know if this is an initial or a confirmed submission?
A: This is done by marking the request with an extra interface.

We have two of them:
1. IInitialSubmission
2. IConfirmedSubmission

Q: When is the IInitialSubmission marker interface set?
A: This is done in fgProcessActionAdapters if no marker interface is set yet.
This then calls getRawActionAdapter, which returns only our
ConfirmedFormMailerAdapter.

Q: When is the IConfirmedSubmission marker interface set?
A: This is done in our confirmation browser view if the confirmation is valid.
If the send_standard_mail field is set in the adapter,
this view first sends a mail like the standard FormMailerAdapter would do.
The confirmation view then calls fgProcessActionAdapters.
This then calls getRawActionAdapter, which returns all except our
ConfirmedFormMailerAdapter.
"""
from collective.confirmableforms.interfaces import IConfirmedFormMailerAdapter
from collective.confirmableforms.interfaces import IConfirmedSubmission
from collective.confirmableforms.interfaces import IInitialSubmission
from zope.interface import alsoProvides


def fgProcessActionAdapters(self, errors, fields=None, REQUEST=None):
    request = REQUEST
    if request is None:
        request = self.REQUEST
    # If this is not a confirmed submission, then it is an initial submission.
    # Mark it as such.
    if not IConfirmedSubmission.providedBy(request):
        alsoProvides(request, IInitialSubmission)
    return self._old_fgProcessActionAdapters(errors, fields=fields, REQUEST=REQUEST)


def getRawActionAdapter(self):
    orig = self._old_getRawActionAdapter()
    if not orig:
        return orig
    initial = IInitialSubmission.providedBy(self.REQUEST)
    confirmed = IConfirmedSubmission.providedBy(self.REQUEST)
    if not (initial or confirmed):
        # Probably the edit form.
        return orig
    # Get a list of action adapters that should be run.
    adapters = []
    for adapter in orig:
        if adapter in adapters:
            continue
        action_adapter = getattr(self.aq_explicit, adapter, None)
        if action_adapter is None:
            continue
        if IConfirmedFormMailerAdapter.providedBy(action_adapter):
            # We should either return only this, or all others.
            if initial:
                # Return only this adapter.
                return (adapter,)
            if confirmed:
                # Ignore this adapter.
                # Note: mail sending is handled by our browser view.
                continue
        adapters.append(adapter)
    return tuple(adapters)
