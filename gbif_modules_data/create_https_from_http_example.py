# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 18:07:31 2020

How to create an https server in few lines

@author: CHRISTIAN
"""

# 1° create yours keys
# openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365

# 2 lauch your web site

import os

if False:
    os.chdir('D:/CreateurENtreprise/src')
    # cd ./to

from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl

from io import BytesIO


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world!')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'This is POST request. ')
        response.write(b'Received: ')
        response.write(body)
        
        
        
httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)

# transform your http adress ontio an https
httpd.socket = ssl.wrap_socket (httpd.socket, 
        keyfile="./to/key.pem", 
        certfile='./to/cert.pem', server_side=True)

httpd.serve_forever()