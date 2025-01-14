from gdltypes import InstallInfo
from shared import shared_events
import subprocess


def clear_mountpoints(installation_object: InstallInfo, root: str):
    shared_events.append(f'Unmounting {root} just in case...')

    process = subprocess.run(['umount', '-Rlf', root], capture_output=True)
    if process.returncode != 0:
        shared_events.append(f'{root} not mounted')
        return

    process = subprocess.run(['umount', '-lf', root], capture_output=True)
    if process.returncode != 0:
        shared_events.append(f'{root} not mounted')
        return

def format_fs(installation_object: InstallInfo, partition_name: str, destination: str, bootable = False):
    partition_device = '/dev/' + partition_name

    process = subprocess.run(['umount', partition_device, destination], capture_output=True)
    if process.returncode != 0:
        shared_events.append(f'{destination} not mounted')
    
    format_args = []

    if bootable:
        format_args = ['mkfs.fat', '-F', '32', partition_device]
    else:
        format_args = ['mkfs.ext4', partition_device]

    process = subprocess.Popen(format_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, universal_newlines=True)
    
    for line in iter(process.stdout.readline, ''):
        shared_events.append(f'Formatting partition: {line.strip()}')
    process.wait()
    
    if process.returncode != 0:
        for line in iter(process.stderr.readline, ''):
            shared_events.append(f'Failed to format {partition_name} partition: {line.strip()}')
        
        return False
    
    return True


def mount_fs(installation_object: InstallInfo, partition_name: str, destination: str):
    partition_device = '/dev/' + partition_name

    process = subprocess.run(['mount', partition_device, destination, '-m'], capture_output=True)
    if process.returncode != 0:
        shared_events.append(f'Failed to mount root partition: {process.stderr.decode()}')
        return False

    shared_events.append(f'Mounted {partition_name} partition to {destination}')

    return True