import json
import sys
import re

if sys.version_info[0] < 3:
    from urlparse import urlparse, urlunparse
else:
    from urllib.parse import urlparse, urlunparse

from websocket import create_connection
from ._transport import Transport


class WebSocketsTransport(Transport):
    def __init__(self, session, connection):
        Transport.__init__(self, session, connection)
        self.ws = None
        self.__requests = {}

    def _get_name(self):
        return 'webSockets'

    @staticmethod
    def __get_ws_url_from(url):
        parsed = urlparse(url)
        scheme = 'wss' if parsed.scheme == 'https' else 'ws'
        url_data = (scheme, parsed.netloc, parsed.path, parsed.params, parsed.query, parsed.fragment)

        return urlunparse(url_data)

    def start(self):
        ws_url = self.__get_ws_url_from(self._get_url('connect'))
        
        proxy_address = None
        if self._session.proxies and ('https' in self._session.proxies or 'http' in self._session.proxies):
            proxy_address = self._session.proxies['https'] or session.proxies['http']
        proxy_data = self.__get_proxy_data(proxy_address)
            
        self.ws = create_connection(ws_url,
                                    header=self.__get_headers(),
                                    cookie=self.__get_cookie_str(),
                                    enable_multithread=True,
                                    http_proxy_host = proxy_data['host'], 
                                    http_proxy_port = proxy_data['port'],
                                    http_proxy_auth = (proxy_data['user'], proxy_data['pass']) if proxy_data['user'] else None)
        
        self._session.get(self._get_url('start'))

        def _receive():
            notification = self.ws.recv()
            self._handle_notification(notification)

        return _receive

    def send(self, data):
        self.ws.send(json.dumps(data))
        #thread.sleep() #TODO: inveistage if we should sleep here or not

    def close(self):
        self.ws.close()

    def accept(self, negotiate_data):
        return bool(negotiate_data['TryWebSockets'])

    class HeadersLoader(object):
        def __init__(self, headers):
            self.headers = headers

    def __get_headers(self):
        headers = self._session.headers
        loader = WebSocketsTransport.HeadersLoader(headers)

        if self._session.auth:
            self._session.auth(loader)

        return ['%s: %s' % (name, headers[name]) for name in headers]

    def __get_cookie_str(self):
        return '; '.join([
                             '%s=%s' % (name, value)
                             for name, value in self._session.cookies.items()
                             ])

    def __get_proxy_data(self, proxy_url):        
        result = {'host': None, 'port': None, 'user': None, 'pass': None}
        
        if proxy_url:
            parts = re.search('((\w+):(\w+)?@)?([\d|\w|.|-]+):(\d{2,5})', proxy_url)
            
            if parts:
                result['user'] = parts.group(2)
                result['pass'] = parts.group(3)
                result['host'] = parts.group(4)
                result['port'] = int(parts.group(5))
            
        return result