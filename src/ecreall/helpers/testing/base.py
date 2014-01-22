from plone.app.testing import login


class FakeResponse(dict):

    redirect_url = None
    status = 404
    headers = None

    def __init__(self):
        self.headers = {}

    def redirect(self, url):
        self.redirect_url = url

    def getStatus(self):
        return self.status

    def setStatus(self, status):
        self.status = status

    def getHeader(self, name):
        return self.headers.get(name, None)

    def setHeader(self, name, value):
        self.headers[name] = value


class FakeRequest(dict):
    debug = False

    def has_key(self, key):
        try:
            self.__getitem__(key)
        except:
            return 0
        else:
            return 1

    def keys(self):
        return self.form.keys()

    def __contains__(self, a):
        return a in self.form or a in self.__dict__

    def get(self, k, default='--MARKER--'):
        if default == '--MARKER--':
            return self.form.get(k, None) or super(FakeRequest, self).get(k)
        else:
            return self.form.get(k, None) or super(FakeRequest, self).get(k, None) or default

    def __getitem__(self, key):
        return self.get(key)

    def __init__(self):
        self.form = {}
        self.response = FakeResponse()
        self.URL = ''

    @property
    def RESPONSE(self):
        return self.response

    @property
    def REQUEST(self):
        return self

    def getURL(self):
        return self.URL


class BaseTest(object):
    """A class with many useful helpers
    """

    def login(self, user):
        login(self.layer['portal'], user)

    def assertLengthEqual(self, list1, length, msg=None):
        self.assertEqual(len(list1), length, msg)

    def assertContainsSame(self, list1, list2, msg=None, key=None):
        return self.assertListEqual(sorted(list1, key=key), sorted(list2, key=key), msg)
