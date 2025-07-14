import dbus
import pyudev
import uuid
from dbus.mainloop.glib import DBusGMainLoop
from threading import Thread
from gi.repository import GLib

SERVICE_NAME = 'org.freedesktop.NetworkManager'
SERVICE_OBJ = '/org/freedesktop/NetworkManager'

BUS = dbus.SystemBus()
UDEV_CONTEXT = pyudev.Context()

def query_internet_devices() -> dict:
    _dict = {}
    nm_proxy = BUS.get_object(SERVICE_NAME, SERVICE_OBJ)
    nm_iface = dbus.Interface(nm_proxy, SERVICE_NAME)

    devices = nm_iface.GetDevices("", "")

    for device in devices:
        device_type = get_device_type(device)

        if device_type == 1:
            _dict[str(device)] = False # Ethernet
        elif device_type == 2:
            _dict[str(device)] = True # Wireless

    return _dict

def get_device_type(device: str) -> int:
    proxy = BUS.get_object(SERVICE_NAME, device)
    props_iface = dbus.Interface(proxy, 'org.freedesktop.DBus.Properties')

    return props_iface.Get(SERVICE_NAME + '.Device', 'DeviceType')

def get_access_points(device: str) -> dbus.Array:
    device_proxy = BUS.get_object(SERVICE_NAME, device)
    device_iface = dbus.Interface(device_proxy, SERVICE_NAME + ".Device.Wireless")

    device_iface.RequestScan(dbus.Dictionary({}))
    access_points = device_iface.GetAllAccessPoints("", "")

    return access_points

def get_access_point_properties(access_points: dbus.Array) -> list[dbus.Dictionary]:
    _list = []
    for ap in access_points:
        proxy = BUS.get_object(SERVICE_NAME, ap)
        props_iface = dbus.Interface(proxy, "org.freedesktop.DBus.Properties")
        props = props_iface.GetAll(SERVICE_NAME + '.AccessPoint')
        props["object"] = ap
        _list.append(props)

    return _list

def get_device_interface_name(device: str):
    proxy = BUS.get_object(SERVICE_NAME, device)
    props_iface = dbus.Interface(proxy, "org.freedesktop.DBus.Properties")
    iface = props_iface.Get(SERVICE_NAME + '.Device', "Interface")
    return iface

def decode_access_point_names(access_points: list) -> None:
    for n, ap in enumerate(access_points):
        for key, value in list(ap.items()):
            if key == "Ssid" and len(value) > 0:
                access_points[n]["decodedSSID"] = bytes(value).decode("utf-8", errors="replace")
                access_points[n][key] = ":".join(str(int(num)) for num in value)

def remove_unused_properties(access_points: list[dict[str, str]]) -> None:
    for n, _ in enumerate(access_points):
        access_points[n].pop("WpaFlags", None)
        access_points[n].pop("RsnFlags", None)
        access_points[n].pop("Frequency", None)
        access_points[n].pop("HwAddress", None)
        access_points[n].pop("MaxBitrate", None)
        access_points[n].pop("Bandwidth", None)
        access_points[n].pop("LastSeen", None)

def sort_and_remove_dublicates_n_empty_ssid(access_points: list[dict[str, str]]) -> list:
    _sorted = sorted(access_points, key=lambda item: item["Strength"], reverse=True)
    _seen = set()
    _clear = []
    for item in _sorted:
        key = item.get("Ssid")
        if key and len(key) > 0 and key not in _seen:
            _seen.add(key)
            _clear.append(item)
    return _clear

def get_internet_devices() -> dict[str, dict[str, str]]:
    devices = query_internet_devices()


    _list: list[str, dict[str, str]] = []
    for device in devices:
        interface = get_device_interface_name(device)
        _list.append({
            "location": device,
            "interface": interface,
            "hardware_name": get_device_hardware_name(interface),
            "wireless": devices[device]
        })
    return _list

def get_device_hardware_name(device_interface: str) -> str:
    for dev in UDEV_CONTEXT.list_devices(subsystem="net"):
        if dev.sys_name == device_interface:
            return dev.get("ID_MODEL_FROM_DATABASE") or "Unknown"
        

def add_connection(SSID: list, password: str):
    proxy = BUS.get_object(SERVICE_NAME, SERVICE_OBJ + '/Settings')
    settings = dbus.Interface(proxy, SERVICE_NAME + '.Settings')

    connection = {
        "connection": {
            "id": dbus.String(bytes(SSID).decode("utf-8", errors="replace")),
            "type": dbus.String("802-11-wireless"),
            "uuid": dbus.String(uuid.uuid4()),
        },
        "802-11-wireless": {
            "ssid": dbus.ByteArray(SSID),
            "mode": dbus.String("infrastructure")
        },
        "ipv4": {
            "method": dbus.String("auto")
        },
        "ipv6": {
            "method": dbus.String("auto")
        }
    }

    if len(password) >= 8:
        connection["802-11-wireless-security"] = {
            "key-mgmt": dbus.String("wpa-psk"),
            "psk": dbus.String(password)
        }

    path = settings.AddConnection(connection)
    return path

def activate_connection(connection: str, device: str, specific_object: str):
    nm_proxy = BUS.get_object(SERVICE_NAME, SERVICE_OBJ)
    nm_iface = dbus.Interface(nm_proxy, SERVICE_NAME)

    return nm_iface.ActivateConnection(connection, device, specific_object)

def get_connectivity():
    nm_proxy = BUS.get_object(SERVICE_NAME, SERVICE_OBJ)
    nm_iface = dbus.Interface(nm_proxy, SERVICE_NAME)

    return nm_iface.CheckConnectivity()

def get_saved_connections():
    nm_proxy = BUS.get_object(SERVICE_NAME, SERVICE_OBJ + '/Settings')
    nm_iface = dbus.Interface(nm_proxy, SERVICE_NAME + '.Settings')

    return nm_iface.ListConnections()

def get_connection_settings(connection: str):
    nm_proxy = BUS.get_object(SERVICE_NAME, connection)
    nm_iface = dbus.Interface(nm_proxy, SERVICE_NAME + '.Settings.Connection')

    return nm_iface.GetSettings()

def delete_connection(connection: str):
    nm_proxy = BUS.get_object(SERVICE_NAME, connection)
    nm_iface = dbus.Interface(nm_proxy, SERVICE_NAME + '.Settings.Connection')

    nm_iface.Delete()

def get_active_connection_state(active_connection: str):
    proxy = BUS.get_object(SERVICE_NAME, active_connection)
    iface = dbus.Interface(proxy, "org.freedesktop.DBus.Properties")

    return iface.Get(SERVICE_NAME + '.Connection.Active', 'State')

def get_device_applied_connection(device: str) -> dict:
    proxy = BUS.get_object(SERVICE_NAME, device)
    device_iface = dbus.Interface(proxy, SERVICE_NAME + '.Device')

    return device_iface.GetAppliedConnection(0)

def disconnect_device(device: str):
    proxy = BUS.get_object(SERVICE_NAME, device)
    device_iface = dbus.Interface(proxy, SERVICE_NAME + '.Device')

    device_iface.Disconnect()

