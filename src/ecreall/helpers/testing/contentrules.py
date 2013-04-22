from AccessControl import getSecurityManager

from plone.app.testing import login, logout
from Products.CMFCore.utils import getToolByName

from workflow import BaseWorkflowTest


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
            self.assertIn("To: %s" % recipient, messages)

        self.assertEqual(len(self._MailHost.messages), len(recipients))
