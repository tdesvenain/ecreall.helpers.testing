from Products.CMFCore.utils import getToolByName

from plone.app.testing import login

class BaseTest(object):
    """A class with many useful helpers to test workflows
    """

    def login(self, user):
        login(self.layer['portal'], user)

    def assertLengthEqual(self, list1, length, msg=None):
        self.assertEqual(len(list1), length, msg)

    def assertContainsSame(self, list1, list2, msg=None, key=None):
        return self.assertListEqual(sorted(list1, key=key), sorted(list2, key=key), msg)
