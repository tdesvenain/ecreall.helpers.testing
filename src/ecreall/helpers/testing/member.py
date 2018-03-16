from plone.app.testing.interfaces import TEST_USER_ID, TEST_USER_NAME
from plone.app.testing import setRoles, login, logout
from plone import api


def createGroups(portal, groupdefs):
    """Create example groups in testing environment

    example_groupdefs = [
        {'group': 'contributeurs', 'roles': ('Contributor',),
        'title': 'Contributeurs', 'groups': ()},
        {'group': 'animateurs', 'roles': ('Reviewer',),
        'title': "Animateurs d'application", 'groups': ()},
        ]

    """
    for groupinfo in groupdefs:
        groupname = groupinfo['group']
        api.group.create(groupname=groupname, roles=groupinfo['roles'])
        group = api.group.get(groupname)
        properties = {'title': groupinfo['title']}
        if 'properties' in groupinfo:
            properties.update(groupinfo.get('properties', {}))

        group.setGroupProperties(properties)

        for supergroup in groupinfo['groups']:
            api.group.add_user(groupname=supergroup, username=groupname)


def createMembers(portal, userdefs, log_in=True):
    """Create example members in testing environment

    example_userdefs = [
            {'user': 'superadmin', 'roles': ('Member', 'Manager'), 'groups': ()},
            {'user': 'membre', 'roles': ('Member', ), 'groups': ()},
            {'user': 'contributeur', 'roles': (), 'groups': ('contributeurs',)},
            {'user': 'animateur', 'roles': (), 'groups': ('animateurs',)},
            ]
    """
    if log_in:
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)

    for userinfo in userdefs:
        username = userinfo['user']
        api.user.create(username=username, email='%s@example.com' % username, roles=userinfo['roles'])
        member = portal.portal_membership.getMemberById(username)
        member.setMemberProperties({'fullname': username.title()})
        for groupname in userinfo['groups']:
            api.group.add_user(groupname=groupname, username=username)

    if log_in:
        setRoles(portal, TEST_USER_ID, ['Member'])
        logout()
