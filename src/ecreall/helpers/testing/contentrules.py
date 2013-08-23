from Products.CMFCore.utils import getToolByName

from workflow import BaseWorkflowTest


def setup_mockmailhost(portal):
    """Use setup_mockmailhost(portal) in your setUpPloneSite method in your
    layer to replace MailHost by a mock.
    """
    from Products.CMFPlone.tests.utils import MockMailHost
    from Products.MailHost.interfaces import IMailHost
    portal.email_from_address = 'portal@example.com'
    mockmailhost = MockMailHost('MailHost')
    portal.MailHost = mockmailhost
    sm = portal.getSiteManager()
    sm.registerUtility(component=mockmailhost, provided=IMailHost)


class BaseContentRulesTest(BaseWorkflowTest):
    """A class with many useful helpers to test content rules
    """

    def contentrules_reset(self):
        from plone.app.contentrules.handlers import _status
        _status.rule_filter.reset()
        MailHost = getToolByName(self.layer['portal'], 'MailHost')
        MailHost.reset()

    def assertNoMessages(self):
        return self.assertRecipientsAre()

    def assertInMessages(self, txt):
        self._MailHost = getattr(self, '_MailHost',
                                getToolByName(self.layer['portal'], 'MailHost'))
        self.assertIn(txt, ' '.join(self._MailHost.messages))

    def assertRecipientsAre(self, *recipients):
        self._MailHost = getattr(self, '_MailHost',
                                getToolByName(self.layer['portal'], 'MailHost'))
        messages = " ".join(self._MailHost.messages)
        for recipient in recipients:
            self.assertIn("To: %s" % recipient, messages, recipient)

        self.assertEqual(len(self._MailHost.messages), len(recipients),
                         "Too many recipients: %s/%s" % (len(recipients),
                                                         len(self._MailHost.messages)))
