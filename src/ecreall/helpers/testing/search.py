from AccessControl import getSecurityManager

from plone.app.testing import login, logout
from Products.CMFCore.utils import getToolByName

from base import BaseTest


class BaseSearchTest(BaseTest):
    """A class with many useful helpers to test workflows
    """

    def getBrain(self, uid):
        ctool = self.portal.portal_catalog
        return ctool.unrestrictedSearchResults(UID=uid)[0]

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
        """Check number of results of a query
        """
        ctool = self.portal.portal_catalog
        self.assertEqual(len(ctool.unrestrictedSearchResults(**query)),
                             results_num)

    def assertSearchFindsInOrder(self, query, ids):
        """Check order of the results
        ids are the ids of documents
        """
        ctool = self.portal.portal_catalog
        result_ids = [b.getId for b in ctool.unrestrictedSearchResults(**query)]
        self.assertListEqual(result_ids, ids)