import time
from logging import getLogger
logger = getLogger('ecreall.profile')

def trace_time(func):
    def wrapper(*__args,**__kw):
        t = time.time()
        try:
            return func(*__args,**__kw)
        finally:
            logger.info( "End for %s in %s" % \
                         (func.__name__,
                          time.strftime('%H h %M m %S.%m sec',
                                        time.gmtime(time.time() - t))))
    return wrapper

def trace_time_content(func):
    def wrapper(*__args,**__kw):
        t = time.time()
        try:
            return func(*__args,**__kw)
        finally:
            logger.info( "End for %s in %s on %s" % \
                         (func.__name__,
                          time.strftime('%H h %M m %S.%m sec',
                                        time.gmtime(time.time() - t)),
                          "/".join(__args[0].getPhysicalPath())))
    return wrapper