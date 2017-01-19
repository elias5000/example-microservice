import BaseHTTPServer
import os
import urllib2
from time import asctime
from urlparse import urlparse

# Config parameters to be set in task definition
apikey = os.environ['APIKEY']
port = int(os.environ['PORT'])

url = 'http://api.openweathermap.org/data/2.5/weather?q={%%s}&APPID=%s' % apikey


class ReqHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def params(self):
        try:
            query = urlparse(self.path).query
            return dict(qc.split("=") for qc in query.split("&"))
        except:
            return dict()

    def do_HEAD(self):
        self.do_GET()

    def do_GET(self):
        try:
            health = self.params()['health']
            if health:
                self.send_response(200)
                self.end_headers()
                self.wfile.write('ok')
                return
        except:
            pass

        try:
            city = self.params()['q']
        except KeyError:
            city = "Berlin"

        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        self.end_headers()
        self.wfile.write(fetch_data(city))


def fetch_data(city):
    doc = urllib2.urlopen(url % city).read()
    return doc


def run(server_class=BaseHTTPServer.HTTPServer, handler_class=ReqHandler):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)

    print asctime(), "Server starts on port %d" % port
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print asctime(), "Server shutting down"
    httpd.server_close()
    print asctime(), "Server stopped"


if __name__ == '__main__':
    run()
