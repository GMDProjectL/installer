import requests
import os
import fcntl
import struct


def get_timezones():
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

def get_drives():
    drives = {}
    for drive in os.listdir('/sys/block'):
        if (not drive.startswith('hd') 
            and not drive.startswith('sd') 
            and not drive.startswith('vd') 
            and not drive.startswith('nvme')):
            continue

        try:
            with open(f'/sys/block/{drive}/device/model', 'r') as f:
                model = f.read().strip()
        except:
            model = 'Unknown Model'
            
        buf = b' ' * 8
        fmt = 'L'
        with open(f'/dev/{drive}') as dev:
            req = 0x80081272
            buf = fcntl.ioctl(dev.fileno(), req, buf)
        size = struct.unpack('L', buf)[0]
        drives[drive] = {
            'model': model,
            'size': size
        }
    return drives

def get_partitions(block_name):
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
            req = 0x80081272
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

def check_internet_connection():
    try:
        r = requests.get("https://archlinux.org")
        return r.status_code == 200
    except:
        return False