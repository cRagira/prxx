from simple_websocket_server import WebSocketServer, WebSocket
import simple_http_server
import urllib
import ssl
from http.server import HTTPServer
from socketserver import ThreadingMixIn
from urllib.parse import urlparse, urlunparse

PORT = 9097

class MyProxy(simple_http_server.SimpleHTTPRequestHandler):
    def do_GET(self):
        url = self.path[1:]
        parsed_url = urlparse(url)
        if parsed_url.scheme == '':
            url = 'http://' + url
        self.send_response(200)
        self.end_headers()
        self.copyfile(urllib.request.urlopen(url), self.wfile)

    def do_POST(self):
        url = self.path[1:]
        parsed_url = urlparse(url)
        if parsed_url.scheme == '':
            url = 'http://' + url
        length = int(self.headers.getheader('content-length'))
        data = self.rfile.read(length)
        req = urllib.request.Request(url, data=data, headers=dict(self.headers))
        response = urllib.request.urlopen(req)
        self.send_response(response.getcode())
        for header, value in response.info().items():
            self.send_header(header, value)
        self.end_headers()
        self.copyfile(response, self.wfile)

    def do_PUT(self):
        url = self.path[1:]
        parsed_url = urlparse(url)
        if parsed_url.scheme == '':
            url = 'http://' + url
        length = int(self.headers.getheader('content-length'))
        data = self.rfile.read(length)
        req = urllib.request.Request(url, data=data, method='PUT', headers=dict(self.headers))
        response = urllib.request.urlopen(req)
        self.send_response(response.getcode())
        for header, value in response.info().items():
            self.send_header(header, value)
        self.end_headers()
        self.copyfile(response, self.wfile)

    def do_DELETE(self):
        url = self.path[1:]
        parsed_url = urlparse(url)
        if parsed_url.scheme == '':
            url = 'http://' + url
        req = urllib.request.Request(url, method='DELETE', headers=dict(self.headers))
        response = urllib.request.urlopen(req)
        self.send_response(response.getcode())
        for header, value in response.info().items():
            self.send_header(header, value)
        self.end_headers()
        self.copyfile(response, self.wfile)

class ThreadingSimpleHTTPSServer(ThreadingMixIn, HTTPServer):
    def __init__(self, server_address, RequestHandlerClass, ssl_certfile, ssl_keyfile):
        HTTPServer.__init__(self, server_address, RequestHandlerClass)
        self.socket = ssl.wrap_socket(self.socket, certfile=ssl_certfile, keyfile=ssl_keyfile, server_side=True)

httpd = ThreadingSimpleHTTPSServer(('', PORT), MyProxy, 'cert.pem', 'key.pem')
print("Now serving at " + str(PORT))
httpd.serve_forever()