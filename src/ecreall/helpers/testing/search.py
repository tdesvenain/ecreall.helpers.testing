import datetime
from DateTime import DateTime

from Products.CMFCore.interfaces import IContentish
from plone.uuid.interfaces import IUUID

from .base import BaseTest


class BaseSearchTest(BaseTest):
    """A class with many useful helpers to test search
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

    def assertSearchFinds(self, query, result):
        """Check number of results of a query
           or check a document is present (by uid or object)
        """
        ctool = self.portal.portal_catalog
        brains = ctool.unrestrictedSearchResults(**query)
        if type(result) == int:
            self.assertEqual(len(brains),
                         result, [r.getPath() for r in brains])
        elif type(result) == str:
            self.assertTrue(result in [r.UID for r in brains],
                "%s document not found in results : %s" % (result,
                                                [r.getPath() for r in brains]))
        elif IContentish.providedBy(result):
            self.assertTrue(IUUID(result) in [r.UID for r in brains],
                "%s document not found in results : %s" % (
                                            '/'.join(result.getPhysicalPath()),
                                            [r.getPath() for r in brains]))
        else:
            raise ValueError("parameter must be an uid or a results num")

    def assertSearchFindsInOrder(self, query, ids):
        """Check order of the results
        ids are the ids of documents
        """
        ctool = self.portal.portal_catalog
        result_ids = [b.getId for b in ctool.unrestrictedSearchResults(**query)]
        self.assertListEqual(result_ids, ids)

    def assertListContains(self, list1, list2):
        self.assertListEqual(sorted(list(list1)), sorted(list(list2)))

    def assertSameDay(self, date1, date2):
        date1, date2 = datify(date1), datify(date2)
        self.assertEqual(date1.Date(), date2.Date())


def datify(s):
    """Get a DateTime object from a string (or anything parsable by DateTime,
       a datetime.date, a datetime.datetime
    """
    if not isinstance(s, DateTime):
        if s == 'None':
            s = None
        elif isinstance(s, datetime.datetime):
            s = DateTime(s.isoformat())
        elif isinstance(s, datetime.date):
            s = DateTime(s.year, s.month, s.day)
        elif s is not None:
            s = DateTime(s)

    return s
