from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess
import requests
import urllib.parse
import os
import json
import fcntl
import struct

req = 0x80081272


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
    
    def get_drives(self):
        drives = {}
        for drive in os.listdir('/sys/block'):
            with open(f'/sys/block/{drive}/device/model', 'r') as f:
                model = f.read().strip()

            buf = b' ' * 8
            fmt = 'L'

            with open(f'/dev/{drive}') as dev:
                buf = fcntl.ioctl(dev.fileno(), req, buf)
            size = struct.unpack('L', buf)[0]

            drives[drive] = {
                'model': model,
                'size': size
            }
        return drives
    
    def get_partitions(self, block_name):
        partition_names = []
        partitions = {}

        for dir in os.listdir(f'/sys/block/{block_name}'):
            if dir.startswith(block_name):
                partition_names.append(dir)
        
        partition_names.sort()

        for partition_name in partition_names:
            buf = b' ' * 8
            fmt = 'L'

            with open(f'/dev/{partition_name}') as dev:
                buf = fcntl.ioctl(dev.fileno(), req, buf)
            size = struct.unpack('L', buf)[0]

            with open(f'/sys/block/{block_name}/{partition_name}/start', 'r') as f:
                start = f.read()
                start = int(start)

            partitions[partition_name] = {
                'size': size,
                'start': start,
            }

        return partitions
    
    def check_internet_connection(self):
        try:
            r = requests.get("https://archlinux.org")
            return r.status_code == 200
        except:
            return False
    

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

        if parsed_path.path == '/get_drives':
            drives = self.get_drives()
            self.wfile.write(json.dumps(drives).encode())

        if parsed_path.path.startswith('/get_partitions/'):
            parts = self.get_partitions(parsed_path.path.replace('/get_partitions/', ''))
            self.wfile.write(json.dumps(parts).encode())
        
        if parsed_path.path == '/check_internet_connection':
            self.wfile.write(json.dumps({'ok': self.check_internet_connection()}).encode())
        
        


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler):
    server_address = ('', 669)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()

run()