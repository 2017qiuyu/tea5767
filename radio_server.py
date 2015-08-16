"""
Programmer	: Dipto Pratyaksa for www.LinuxCircle.com
Dependencies	: tea5767stationscanner.py, index.html
Original source	: http://www.svesoftware.com/documents/radio_server.py
Last update	: 17 August 2015 - Indonesia's independence day
"""

import sys
import http
from http import server
import os
import glob
import time
import datetime
import tea5767stationscanner

import sys

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    
    tea = None

    def __init__(self, request, address, server):
        self.tea = tea5767stationscanner.tea5767()
        http.server.SimpleHTTPRequestHandler.__init__(self, request, address, server)		


    def do_GET(self):
        if self.path == '/':
            self.path = 'index.html'
        if self.path == '/searchup':
            self.tea.scan(1)
            print('search up finished')
            self.send_response(200)
            self.send_header('Content-type','text/html')
            #self.send_header("Content-type", "application/json")
            #self.send_header("Content-length", 2)
            self.end_headers()
            self.wfile.write(bytes("ok","UTF-8"))
            self.wfile.flush()
            return
        if self.path == '/searchdown':
            self.tea.scan(0)
            print('search down finished')
            self.send_response(200)
            self.send_header('Content-type','text/html')
            #self.send_header("Content-type", "application/json")
            #self.send_header("Content-length", 2)
            self.end_headers()
            self.wfile.write(bytes("ok","UTF-8"))
            self.wfile.flush()
            return
        if self.path == '/off':
            self.tea.off()
            print('radio mute')
            self.send_response(200)
            self.send_header('Content-type','text/html')
            #self.send_header("Content-type", "application/json")
            #self.send_header("Content-length", 2)
            self.end_headers()
            self.wfile.write(bytes("ok","UTF-8"))
            self.wfile.flush()
            return

        if self.path == '/info':
            resp = self.tea.info()
            resp = "{" + '"freq":' + resp['freq'] + ',"level":' + resp['level']  + "}"
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Content-length", len(resp))
            self.end_headers()
            self.wfile.write(bytes(resp, 'UTF-8'))
            return

        return http.server.SimpleHTTPRequestHandler.do_GET(self)
     
    
      
HandlerClass = MyRequestHandler
ServerClass  = http.server.HTTPServer
Protocol     = "HTTP/1.0"



if sys.argv[1:]:
    port = int(sys.argv[1])
else:
    port = 10005
server_address = ('0.0.0.0', port)

HandlerClass.protocol_version = Protocol
httpd = ServerClass(server_address, HandlerClass)

sa = httpd.socket.getsockname()
print ("Serving HTTP on ", sa[0], "port", sa[1])
httpd.serve_forever()



