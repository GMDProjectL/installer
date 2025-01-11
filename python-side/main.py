from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import os
import json


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def get_timezones(self):
        timezones = {}
        for root, dirs, files in os.walk('/usr/share/zoneinfo'):
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                if dir_path.startswith('/usr/share/zoneinfo/'):
                    dir_name = dir_path.split('/')[-1]
                    timezones[dir_name] = []
                    for _, _, files in os.walk(dir_path):
                        for file in files:
                            if not file.startswith('.'):
                                timezones[dir_name].append(file)
        return timezones

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

        if parsed_path.path == '/get_timezones':
            timezones = self.get_timezones()
            self.wfile.write(json.dumps(timezones).encode())



def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler):
    server_address = ('', 669)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()

run()