# coding=utf-8

import BaseHTTPServer
import os
import urllib2
from time import asctime
from urlparse import urlparse
import json

# Config parameters to be set in task definition
port = int(os.environ['PORT'])
url = "http://%s:%d/?q=%%s" % (os.environ['API_HOST'], int(os.environ['API_PORT']))
server_type = os.environ['TYPE']
try:
    host = os.environ['HOSTNAME']
except:
    host = 'unknown'

page = '''
<html>
    <header>
        <title>Weather API Demo</title>
        <style type="text/css">
            body {
                background: #fff;
                text-align: center;
                font-family: sans-serif;
            }
            div {
                width: 300px;
                margin: auto;
            }
            #data {
                border: 3px solid black;
                border-radius: 25px;
                font-size: 50px;
            }
            #meta {
                font-size: 20px;
            }
            h1 {
                font-size: 35px;
                background: #ccc;
            }
        </style>
    </header>
    <body>
        <div id="data">
            <h1>%s</h1>
            <p>%s</p>
        </div>
        <div id="meta">
            <p>Container ID: %s</p>
        </div>
    </body>
</html>
'''


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

        try:
            get_data(city)
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(page % (city, get_data(city), host))

        except Exception as e:
            print asctime(), e
            self.send_response(500)
            self.end_headers()
            self.wfile.write('500 - Could not respond your request.')


def get_data(city):
    doc = urllib2.urlopen(url % city).read()

    if server_type == 'temp':
        return "%.1f°C" % float(json.loads(doc)['main']['temp'] - 273.15)
    elif server_type == 'pressure':
        return "%d hPa" % int(json.loads(doc)['main']['pressure'])
    elif server_type == 'wind':
        return "%.1f m/s" % float(json.loads(doc)['wind']['speed'])


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
