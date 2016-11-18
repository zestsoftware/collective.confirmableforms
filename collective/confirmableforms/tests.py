from Products.Five import fiveconfigure
from Products.Five import zcml
from Products.Five.testbrowser import Browser
from Products.MailHost.interfaces import IMailHost
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from Products.SecureMailHost.SecureMailHost import SecureMailHost as MailBase
from Testing import ZopeTestCase as ztc
from Testing.ZopeTestCase.zopedoctest import ZopeDocFileSuite
from zope.component import getSiteManager

import collective.confirmableforms
import doctest
import Products.PloneFormGen
import unittest


ptc.setupPloneSite()
OPTIONFLAGS = (doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)


class MockMailHost(MailBase):
    """A MailHost that collects messages instead of sending them.

    Thanks to Rocky Burt for inspiration.
    """

    def __init__(self, id):
        MailBase.__init__(self, id, smtp_notls=True)
        self.reset()

    def reset(self):
        self.messages = []

    def send(self, message, mto=None, mfrom=None, subject=None, encode=None):
        """
        Basically construct an email.Message from the given params to make sure
        everything is ok and store the results in the messages instance var.
        """
        self.messages.append(message)

    def secureSend(self, message, mto, mfrom, **kwargs):
        kwargs['debug'] = True
        result = MailBase.secureSend(self, message=message, mto=mto,
                                     mfrom=mfrom, **kwargs)
        self.messages.append(result)

    def validateSingleEmailAddress(self, address):
        return True  # why not


class TestCase(ptc.FunctionalTestCase):

    def __init__(self, *args, **kwargs):
        super(TestCase, self).__init__(*args, **kwargs)
        self.browser = Browser()

    class layer(PloneSite):

        @classmethod
        def setUp(cls):
            pass

        @classmethod
        def tearDown(cls):
            pass

    def install_pfg(self):
        fiveconfigure.debug_mode = True
        zcml.load_config('configure.zcml',
                         Products.PloneFormGen)

        ztc.installPackage(Products.PloneFormGen)
        self.addProfile('Products.PloneFormGen:default')

        fiveconfigure.debug_mode = False

    def install_confirmableforms(self):
        fiveconfigure.debug_mode = True
        zcml.load_config('configure.zcml',
                         collective.confirmableforms)

        ztc.installPackage(collective.confirmableforms)
        self.addProfile('collective.confirmableforms:default')

        ztc.installPackage(collective.confirmableforms)
        fiveconfigure.debug_mode = False

    def afterSetUp(self):
        self.portal._original_MailHost = self.portal.MailHost
        self.portal.MailHost = mailhost = MockMailHost('MailHost')
        sm = getSiteManager(context=self.portal)
        sm.unregisterUtility(provided=IMailHost)
        sm.registerUtility(mailhost, provided=IMailHost)

        # This hack allows us to get the traceback when an
        # 500 error is raised while using the browser.
        self.portal.error_log._ignored_exceptions = ()

        def raising(self, info):
            import traceback
            traceback.print_tb(info[2])
            print info[1]

        from Products.SiteErrorLog.SiteErrorLog import SiteErrorLog
        SiteErrorLog.raising = raising

    def login_as_user(self, username, password):
        portal_url = self.portal.absolute_url()

        self.browser.open('%s/logout' % portal_url)
        self.browser.open('%s/login_form' % portal_url)
        self.browser.getControl(name='__ac_name').value = username
        self.browser.getControl(name='__ac_password').value = password
        self.browser.getControl(name='submit').click()

    def login_as_manager(self):
        self.login_as_user(ptc.portal_owner,
                           ptc.default_password)


def test_suite():
    return unittest.TestSuite([
        ZopeDocFileSuite(
            'tests.txt',
            package='collective.confirmableforms',
            optionflags=OPTIONFLAGS,
            test_class=TestCase),

        # Unit tests
        # doctestunit.DocFileSuite(
        #    'README.txt', package='collective.confirmableforms',
        #    setUp=testing.setUp, tearDown=testing.tearDown),

        # doctestunit.DocTestSuite(
        #    module='collective.confirmableforms.mymodule',
        #    setUp=testing.setUp, tearDown=testing.tearDown),


        # Integration tests that use PloneTestCase
        # ztc.ZopeDocFileSuite(
        #    'README.txt', package='collective.confirmableforms',
        #    test_class=TestCase),

        # ztc.FunctionalDocFileSuite(
        #    'browser.txt', package='collective.confirmableforms',
        #    test_class=TestCase),

    ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
