from AccessControl import getSecurityManager

from plone.app.testing import login, logout
from Products.CMFCore.utils import getToolByName

from .base import BaseTest


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


class BaseWorkflowTest(BaseTest):
    """A class with many useful helpers to test workflows
    """


    def doActionFor(self, doc, action, **kwargs):
        self.portal.portal_workflow.doActionFor(doc, action, **kwargs)

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
