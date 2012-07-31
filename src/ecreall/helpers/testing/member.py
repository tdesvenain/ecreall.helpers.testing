from plone.app.testing.interfaces import TEST_USER_ID, TEST_USER_NAME
from plone.app.testing import setRoles, login, logout

def addMember(pas, username, fullname="", email="", roles=('Member',)):
    """Create an new member.

    The password is always 'secret'.
    """
    pas.userFolderAddUser(username, 'secret', roles, [])


def addGroup(gtool, groupid, roles=('Member',)):
    """Create an new group.

    The password is always 'secret'.
    """
    gtool.addGroup(groupid, roles=('Member',))


def createGroups(portal, groupdefs):
    """Create example groups in testing environment

    example_groupdefs = [
        {'group': 'contributeurs', 'roles': ('Contributor',),
        'title': 'Contributeurs', 'groups': ()},
        {'group': 'animateurs', 'roles': ('Reviewer',),
        'title': "Animateurs d'application", 'groups': ()},
        ]

    """
    gtool = portal.portal_groups
    for groupinfo in groupdefs:
        groupname = groupinfo['group']
        addGroup(gtool, groupname, roles=groupinfo['roles'])
        group = gtool.getGroupById(groupname)
        group.setGroupProperties({'title': groupinfo['title']})
        for supergroup in groupinfo['groups']:
            gtool.getGroupById(supergroup).addMember(groupname)

def createMembers(portal, userdefs):
    """Create example members in testing environment

    example_userdefs = [
            {'user': 'superadmin', 'roles': ('Member', 'Manager'), 'groups': ()},
            {'user': 'membre', 'roles': ('Member', ), 'groups': ()},
            {'user': 'contributeur', 'roles': (), 'groups': ('contributeurs',)},
            {'user': 'animateur', 'roles': (), 'groups': ('animateurs',)},
            ]
"""
    setRoles(portal, TEST_USER_ID, ['Manager'])
    login(portal, TEST_USER_NAME)

    pas = portal.acl_users
    gtool = portal.portal_groups
    for userinfo in userdefs:
        username = userinfo['user']
        addMember(pas, username, roles=userinfo['roles'])
        member = portal.portal_membership.getMemberById(username)
        member.setMemberProperties({'email': '%s@example.com' % username,
                                    'fullname': username.title()})
        for groupname in userinfo['groups']:
            group = gtool.getGroupById(groupname)
            group.addMember(username)

    ged = portal.ged
    media = portal.media

    ged.manage_setLocalRoles('contributeurs', ('Contributor',))
    ged.manage_setLocalRoles('animateurs', ('Reviewer',))
    ged.reindexObjectSecurity()

    media.manage_setLocalRoles('contributeurs', ('Contributor',))
    media.manage_setLocalRoles('animateurs', ('Reviewer',))
    media.reindexObjectSecurity()

    setRoles(portal, TEST_USER_ID, ['Member'])
    logout()
