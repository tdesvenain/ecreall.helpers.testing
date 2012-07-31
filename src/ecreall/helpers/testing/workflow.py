from AccessControl import getSecurityManager

from plone.app.testing import login, logout

def assertCheckPermissions(portal, obj, permissions, user_defs, stateid=None,
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

    self.assertFalse(msg)