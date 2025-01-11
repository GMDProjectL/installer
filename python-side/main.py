from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from utils import check_internet_connection, get_drives, get_partitions, get_timezones
from installation import start_installation


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):


    def handle_cors(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        parsed_path = self.path
        self.handle_cors()

        if parsed_path == '/get_timezones':
            self.wfile.write(json.dumps(get_timezones()).encode())

        if parsed_path == '/get_drives':
            self.wfile.write(json.dumps(get_drives()).encode())

        if parsed_path.startswith('/get_partitions/'):
            drive = parsed_path.split('/')[-1]
            self.wfile.write(json.dumps(get_partitions(drive)).encode())
        
        if parsed_path == '/check_internet_connection':
            self.wfile.write(json.dumps({'ok': check_internet_connection()}).encode())
    

    def do_POST(self):
        parsed_path = self.path

        if parsed_path == '/install':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            install_object = json.loads(body)
            start_installation(install_object)


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler):
    server_address = ('', 669)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()

run()