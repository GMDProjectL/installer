from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from utils import check_internet_connection, get_drives, get_partitions, get_timezones
from installation import start_installation
import threading
from shared import shared_progress,shared_events 
from gdltypes import InstallInfo
import os
import systemd.daemon

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
        
        if parsed_path == '/get_installation_events':
            self.wfile.write(json.dumps({'events': shared_events}).encode())
            shared_events.clear()
        
        if parsed_path == '/get_installation_progress':
            self.wfile.write(json.dumps({'progress': len(shared_progress), 'total': 30}).encode())
        
        if parsed_path == '/reboot':
            self.wfile.write(json.dumps({'ok': True}).encode())
            os.system("reboot")

    def do_OPTIONS(self):
        self.handle_cors()    

    def do_POST(self):
        parsed_path = self.path
        self.handle_cors()

        if parsed_path == '/install':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            install_object = json.loads(body)
            self.wfile.write(json.dumps({'ok': True}).encode())
            threading.Thread(target=start_installation, args=(InstallInfo(**install_object),)).start()


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler):
    server_address = ('', 669)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    systemd.daemon.notify('READY=1')
    httpd.serve_forever()

run()