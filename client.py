import urllib2


class HttpClient:
    def __init__(self, proxy = {}, timeout = None):
        self.__proxy = proxy
        self.__timeout = timeout

    def get_response(self, url):
        if len(self.__proxy) > 0:
            proxy = urllib2.ProxyHandler(self.__proxy)
            opener = urllib2.build_opener(proxy)
            urllib2.install_opener(opener)

        u = None
        if self.__timeout is None:
            u = urllib2.urlopen(url)
        else:
            u = urllib2.urlopen(url, timeout=self.__timeout)
        
        return u.read()