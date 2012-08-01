from AccessControl import getSecurityManager

from plone.app.testing import login, logout
from Products.CMFCore.utils import getToolByName


def verifyPermissions(portal, obj, permissions, user_defs, stateid=None,
                           ignore_members=()):
    orig_username = getSecurityManager().getUser().getUserName()

    failed = {}
    for permission in permissions:
        failed[permission] = []

    for uinfo in user_defs:
        user = uinfo['user']
        if user in ignore_members:
            continue

        login(portal, user)
        m = getSecurityManager()
        for permission, authorized_users in permissions.items():
            has_perm = bool(m.checkPermission(permission, obj))
            if has_perm ^ (user in authorized_users):
                failed[permission].append(
                    (user, has_perm, m.getUser().getRolesInContext(obj),)
                    )
        logout()

#    if orig_userid != 'Anonymous User':
    login(portal, orig_username)

    msg = ''
    for permission in permissions:
        if failed[permission]:
            msg += 'Problem with "%s" for users%s:\n%s\n' \
                   % (permission,
                   stateid and " (state=%s)" % stateid or "",
                   '\n'.join([repr(i) for i in failed[permission]]),
                   )

    return msg


class BaseWorkflowTest(object):
    """A class with many useful helpers to test workflows
    """


    def contentrules_reset(self):
        from plone.app.contentrules.handlers import _status
        _status.rule_filter.reset()
        MailHost = getToolByName(self.layer['portal'], 'MailHost')
        MailHost.reset()

    def login(self, user):
        login(self.portal, user)

    def doActionFor(self, doc, action, **kwargs):
        self.portal.portal_workflow.doActionFor(doc, action, **kwargs)

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

    def assertLengthEqual(self, list1, length, msg=None):
        self.assertEqual(len(list1), length, msg)

    def assertCanFind(self, document):
        """Check if user can find document through a catalog search
        """
        ctool = self.portal.portal_catalog
        self.assertEqual(len(ctool.searchResults(UID=document.UID())), 1)

    def assertCanNotFind(self, document):
        """Check if user can find document through a catalog search
        """
        ctool = self.portal.portal_catalog
        self.assertEqual(len(ctool.searchResults(UID=document.UID())), 0)

    def assertSearchFinds(self, query, results_num):
        ctool = self.portal.portal_catalog
        self.assertEqual(len(ctool.unrestrictedSearchResults(**query)),
                             results_num)

    def assertCheckPermissions(self, doc, permissions, user_defs, stateid=None,
                               ignore_members=()):
        # todo: put the code here

        msg = verifyPermissions(self.portal, doc, permissions, user_defs,
                                stateid=stateid, ignore_members=ignore_members)
        self.assertTrue(len(msg)==0, msg)

    def assertHasState(self, doc, state, msg=None):
        wtool = getToolByName(doc, 'portal_workflow')
        doc_state = wtool.getInfoFor(doc, 'review_state')
        self.assertEqual(doc_state, state, msg or
                  "Document state is %s, it should be %s." % (doc_state, state))

    def assertHasLifeCycleState(self, doc, state, msg=None):
        doc_state = ILifeCycleInfo(doc).state
        self.assertEqual(doc_state, state, msg or
        "Document lifecycle state is %s, it should be %s." % (doc_state, state))

    def assertContainsSame(self, list1, list2, msg=None, key=None):
        return self.assertListEqual(sorted(list1, key=key), sorted(list2, key=key), msg)
