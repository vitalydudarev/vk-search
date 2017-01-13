import urllib2
from socket import timeout


class HttpClient:
    def __init__(self, proxy = {}, timeout = None):
        self.__proxy = proxy
        self.__timeout = timeout

    def get_response(self, url):
        if len(self.__proxy) > 0:
            proxy = urllib2.ProxyHandler(self.__proxy)
            opener = urllib2.build_opener(proxy)
            urllib2.install_opener(opener)

        has_error = False
        response_text = ""

        try:
            u = None
            if self.__timeout is None:
                u = urllib2.urlopen(url)
            else:
                u = urllib2.urlopen(url, timeout=self.__timeout)
            response_text = u.read()

        except (urllib2.HTTPError, urllib2.URLError) as error:
            has_error = True
        except timeout:
            has_error = True

        return Response(has_error, response_text)


class Response:
    def __init__(self, has_error, response_text):
        self.has_error = has_error
        self.response_text = response_text