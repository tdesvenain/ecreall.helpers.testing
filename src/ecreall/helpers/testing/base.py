from plone.app.testing import login


class FakeResponse(dict):

    redirect_url = None
    def redirect(self, url):
        self.redirect_url = url


class FakeRequest(dict):

    def __init__(self):
        self.form = {}
        self.response = FakeResponse()

    @property
    def RESPONSE(self):
        return self.response


class BaseTest(object):
    """A class with many useful helpers
    """

    def login(self, user):
        login(self.layer['portal'], user)

    def assertLengthEqual(self, list1, length, msg=None):
        self.assertEqual(len(list1), length, msg)

    def assertContainsSame(self, list1, list2, msg=None, key=None):
        return self.assertListEqual(sorted(list1, key=key), sorted(list2, key=key), msg)
