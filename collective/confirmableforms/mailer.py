# This was stolen from Maurits van Rees code for collective.watcherlist
# https://github.com/collective/collective.watcherlist/blob/master/collective/watcherlist/mailer.py

from collective.confirmableforms import utils
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from Products.MailHost.MailHost import MailHostError
from smtplib import SMTPException

import logging
import pkg_resources
import socket


logger = logging.getLogger('collective.confirmableforms')

zope2_egg = pkg_resources.working_set.find(
    pkg_resources.Requirement.parse('Zope2'))
USE_SECURE_SEND = True
if zope2_egg and (zope2_egg.parsed_version >=
                  pkg_resources.parse_version('2.12.3')):
    USE_SECURE_SEND = False


def simple_send_mail(plain, html, addresses, mfrom, subject, immediate=True):
    """Send a notification email to the list of addresses.

    The method is called 'simple' because all the clever stuff should
    already have been done by the caller.

    message is passed without change to the mail host.  It should
    probably be a correctly encoded Message or MIMEText.

    One mail with the given message and subject is sent for each address.

    Note that with Plone 4 (Zope 2.12) by default the sending is
    deferred to the end of the transaction.  This means an exception
    would roll back the transaction.  We usually do not want that, as
    the email sending is an extra: we do not mind too much if sending
    fails.  Luckily we have the option to send immediately, so we can
    catch and ignore exceptions.  In this method we do that.  You can
    override that by passing immediate=False.  Note that in Plone 3
    this has no effect at all.
    """
    mail_host = utils.get_mail_host()
    if mail_host is None:
        logger.warn("Cannot send notification email: please configure "
                    "MailHost correctly.")
        # We print some info, which is perfect for checking in unit
        # tests.
        print 'Subject =', subject
        print 'Addresses =', addresses
        print 'Message ='
        print plain
        return

    if not mfrom:
        mfrom = utils.get_mail_from_address()

    header_charset = utils.get_charset()

    text_part = MIMEText(plain, 'plain', header_charset)
    html_part = MIMEText(html, 'html', header_charset)

    if plain and html:
        email_content = MIMEMultipart('alternative')
        email_content.epilogue = ''
        email_content.attach(text_part)
        email_content.attach(html_part)
    elif plain:
        email_content = text_part
    elif html:
        email_content = html_part
    else:
        # Hm, that's weird.
        email_content = ''

    for address in addresses:
        if not address:
            continue
        try:
            if USE_SECURE_SEND:
                mail_host.secureSend(message=email_content,
                                     mto=address,
                                     mfrom=mfrom,
                                     subject=subject,
                                     charset=header_charset)
            else:
                mail_host.send(email_content,
                               mto=address,
                               mfrom=mfrom,
                               subject=subject,
                               immediate=immediate,
                               charset=header_charset)
        except (socket.error, SMTPException, MailHostError):
            logger.warn('Could not send email to %s with subject %s',
                        address, subject)
        except:
            raise
