from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from utils import get_drives, get_partitions, get_timezones, genUUID
from installation import start_safe_installation, start_safe_update
import threading
from shared import shared_progress,shared_events 
from gdltypes import InstallInfo, UpdateFlags
import os
import systemd.daemon
import base.nm_dbus as nm_dbus
import dbus
from urllib.parse import urlparse, parse_qs

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def handle_cors(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        url = urlparse(self.path)

        if url.path == '/get_internet_devices':
            self.handle_cors()
            self.wfile.write(json.dumps(nm_dbus.get_internet_devices()).encode())

        if url.path == '/get_access_points':
            query = parse_qs(url.query)
            points: dbus.Array
            try:
                points = nm_dbus.get_access_points(query.get("device", [''])[0])
                properties = nm_dbus.get_access_point_properties(points)
                nm_dbus.decode_access_point_names(properties)
                nm_dbus.remove_unused_properties(properties)
                result = nm_dbus.sort_and_remove_dublicates_n_empty_ssid(properties)

                self.handle_cors()
                self.wfile.write(json.dumps(result, default=str).encode())
            except Exception:
                self.send_error(428, "No or bad wlan device!", "Please provide proper device query variable")
        
        if url.path == '/check_connectivity':
            result = nm_dbus.get_connectivity()

            self.handle_cors()
            self.wfile.write(json.dumps(result, default=str).encode())

        if url.path == '/list_connections':
            result = nm_dbus.get_saved_connections()

            self.handle_cors()
            self.wfile.write(json.dumps(result, default=str).encode())

        if url.path == '/get_connection_settings':
            query = parse_qs(url.query)

            result = nm_dbus.get_connection_settings(query.get("connection")[0])

            self.handle_cors()
            self.wfile.write(json.dumps(result, default=str).encode())

        if url.path == '/get_active_connection_state':
            query = parse_qs(url.query)
            
            try:
                result = nm_dbus.get_active_connection_state(query.get("connection")[0])
            except dbus.exceptions.DBusException as e:
                if e.get_dbus_name() == "org.freedesktop.DBus.Error.UnknownMethod":
                    result = "UnknownMethod"

            self.handle_cors()
            self.wfile.write(json.dumps(result, default=str).encode())

        if url.path == '/get_applied_connection':
            query = parse_qs(url.query)

            result = None

            try:
                result = nm_dbus.get_device_applied_connection(query.get("device", [''])[0])
            except dbus.exceptions.DBusException as e:
                if e.get_dbus_name() == 'org.freedesktop.NetworkManager.Device.NotActive':
                    result = "NotActive"

            self.handle_cors()
            self.wfile.write(json.dumps(result, default=str).encode())

        if url.path == '/update':
            query = parse_qs(url.query)
            result = {}

            check_connectivity = query.get("check_connectivity", [False])[0].lower() == "true"
            list_connections = query.get("list_connections", [False])[0].lower() == "true"
            get_access_points = query.get("get_ap", [False])[0].lower() == "true"
            get_applied_connection = query.get("get_applied_connection", [False])[0].lower() == "true"       

            if check_connectivity:
                result["connectivity"] = nm_dbus.get_connectivity()

            if list_connections:
                _result = []

                connections = nm_dbus.get_saved_connections()

                for connection in connections:
                    __result = nm_dbus.get_connection_settings(connection)
                    __result["connection"]["location"] = connection

                    _result.append(__result)

                result["saved_connections"] = _result

            if get_access_points:
                device = query.get("device", [''])[0]
                aps = nm_dbus.get_access_points(device)
                properties = nm_dbus.get_access_point_properties(aps)
                nm_dbus.decode_access_point_names(properties)
                nm_dbus.remove_unused_properties(properties)
                result["access_points"] = nm_dbus.sort_and_remove_dublicates_n_empty_ssid(properties)
            
            if get_applied_connection:
                try:
                    device = query.get("device", [''])[0]
                    result["applied_connection"] = nm_dbus.get_device_applied_connection(device)[0]["connection"]
                    result["applied_connection"]["active_loc"] = nm_dbus.get_device_applied_connection(device)[1]
                except dbus.exceptions.DBusException as e:
                    if e.get_dbus_name() == "org.freedesktop.NetworkManager.Device.NotActive":
                        result["applied_connection"] = "undefined"
            
            self.handle_cors()
            self.wfile.write(json.dumps(result, default=str).encode())

        if url.path == '/get_timezones':
            self.handle_cors()
            self.wfile.write(json.dumps(get_timezones()).encode())

        if url.path == '/get_drives':
            self.handle_cors()
            self.wfile.write(json.dumps(get_drives()).encode())
        
        if url.path == '/get_system_language':
            self.handle_cors()
            self.wfile.write(json.dumps({"lang": os.getenv("LANG")}).encode())

        if url.path.startswith('/get_partitions/'):
            drive = url.path.split('/')[-1]
            self.handle_cors()
            self.wfile.write(json.dumps(get_partitions(drive)).encode())
        
        if url.path == '/get_installation_events':
            self.handle_cors()
            self.wfile.write(json.dumps({'events': shared_events}).encode())
            shared_events.clear()
        
        if url.path == '/get_installation_progress':
            self.handle_cors()
            self.wfile.write(json.dumps({'progress': len(shared_progress), 'total': 30}).encode())
        
        if url.path == '/reboot':
            self.handle_cors()
            self.wfile.write(json.dumps({'ok': True}).encode())
            os.system("reboot")

    def do_OPTIONS(self):
        self.handle_cors()    

    def do_POST(self):
        url = urlparse(self.path)
        
        if url.path == '/add_connection':
            content_length = int(self.headers['Content-Length'])
            body_json = json.loads(self.rfile.read(content_length))
            ssid: str = body_json["Ssid"]
            password: str = body_json["password"]

            _list = ssid.split(":")

            int_list = [int(e) for e in _list]

            path = nm_dbus.add_connection(int_list, password)
            self.handle_cors()
            self.wfile.write(json.dumps({'path': path}).encode())

        if url.path == '/activate_connection':
            content_length = int(self.headers['Content-Length'])
            body_json = json.loads(self.rfile.read(content_length))

            connection = body_json["connection"]
            
            print(connection)

            specific_obj = body_json["object"]
            device = body_json["device"]

            result = nm_dbus.activate_connection(connection, device, specific_obj)

            self.handle_cors()
            self.wfile.write(json.dumps(result, default=str).encode())

        if url.path == '/delete_connection':
            content_length = int(self.headers['Content-Length'])
            body_json = json.loads(self.rfile.read(content_length))

            connection = body_json["connection"]

            nm_dbus.delete_connection(connection)

            self.handle_cors()

        if url.path == '/disconnect_device':
            content_length = int(self.headers['Content-Length'])
            body_json = json.loads(self.rfile.read(content_length))

            device = body_json["device"]
            nm_dbus.disconnect_device(device)
            self.handle_cors()
            
        if url.path == '/install':
            content_length = int(self.headers['Content-Length'])
            body_json = self.rfile.read(content_length)
            install_object = json.loads(body_json)
            self.handle_cors()
            self.wfile.write(json.dumps({'ok': True}).encode())
            threading.Thread(target=start_safe_installation, args=(
                InstallInfo(fromUpdate=False, **install_object)
            ,)).start()
        
        if url.path == '/update':
            content_length = int(self.headers['Content-Length'])
            body_json = self.rfile.read(content_length)
            update_flags_json: dict = json.loads(body_json)
            self.handle_cors()
            self.wfile.write(json.dumps({'ok': True}).encode())

            update_flags = UpdateFlags(
                "kde", 
                False, 
                False, 
                False, 
                False, 
                False, 
                False, 
                False, 
                False, 
                False, 
                False, 
                False, 
                False, 
                False, 
                True, 
                "myuser", 
                False, 
                False,
                False
            )
            
            for flag in update_flags_json.keys():
                try:
                    update_flags.__setattr__(flag, update_flags_json[flag])
                    print(f"Set {flag} flag")
                except Exception as e:
                    print(f"Skipping {flag} flag")
            
            update_flags.fromUpdate = True

            threading.Thread(target=start_safe_update, args=(update_flags,)).start()


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler):
    server_address = ('', 669)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    systemd.daemon.notify('READY=1')
    httpd.serve_forever()

run()