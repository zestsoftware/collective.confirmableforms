# All code related to emails is taken from collective.watcherlist
# https://github.com/collective/collective.watcherlist/blob/master/collective/watcherlist/utils.py

try:
    from email.utils import parseaddr, formataddr
    parseaddr, formataddr  # pyflakes
except ImportError:
    # BBB for python2.4 (Plone 3)
    from email.Utils import parseaddr, formataddr

from persistent.dict import PersistentDict
from persistent.list import PersistentList
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from zope.component import getMultiAdapter


try:
    from zope.component.hooks import getSite
    getSite  # pyflakes
except ImportError:
    from zope.app.component.hooks import getSite


DEFAULT_CHARSET = 'utf-8'


def get_charset():
    """Character set to use for encoding the email.

    If encoding fails we will try some other encodings.  We hope
    to get utf-8 here always actually.

    The getSiteEncoding call also works when portal is None, falling
    back to utf-8.  But that is only on Plone 4, not Plone 3.  So we
    handle that ourselves.
    """
    charset = None
    portal = getSite()
    if portal is None:
        return DEFAULT_CHARSET
    charset = portal.getProperty('email_charset', '')
    if not charset:
        charset = 'utf-8'
    return charset


def su(value):
    """Return safe unicode version of value.
    """
    return safe_unicode(value, encoding=get_charset())


def get_mail_host():
    """Get the MailHost object.

    Return None in case of problems.
    """
    portal = getSite()
    if portal is None:
        return None
    request = portal.REQUEST
    ctrlOverview = getMultiAdapter((portal, request),
                                   name='overview-controlpanel')
    mail_settings_correct = not ctrlOverview.mailhost_warning()
    if mail_settings_correct:
        mail_host = getToolByName(portal, 'MailHost', None)
        return mail_host


def get_mail_from_address():
    portal = getSite()
    if portal is None:
        return ''
    from_address = portal.getProperty('email_from_address', '')
    from_name = portal.getProperty('email_from_name', '')
    mfrom = formataddr((from_name, from_address))
    if parseaddr(mfrom)[1] != from_address:
        # formataddr probably got confused by special characters.
        mfrom = from_address
    return mfrom


def obj_to_pobj(o):
    """ Return an object to a persistent object.
    Only works on list and dictionaries for now.
    """

    if isinstance(o, list):
        return list_to_plist(o)

    if isinstance(o, dict):
        return dict_to_pdict(o)

    return o


def list_to_plist(l):
    pl = PersistentList()
    for val in l:
        pl.append(obj_to_pobj(val))

    return pl


def dict_to_pdict(d):
    pd = PersistentDict()

    for k, v in d.items():
        pd[obj_to_pobj(k)] = obj_to_pobj(v)

    return pd
