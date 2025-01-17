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


def nuke_drive(installation_object: InstallInfo, drive_name: str):
    shared_events.append(f'Nuking {drive_name} drive...')
    process = subprocess.run(['wipefs', '-a', '/dev/' + drive_name], capture_output=True)
    if process.returncode != 0:
        shared_events.append(f'Failed to wipefs {drive_name} drive: {process.stderr.decode()}')
    
    shared_events.append("wipefs: " + process.stdout.decode())
    
    process = subprocess.run(['parted', '/dev/' + drive_name, '--script', 'mklabel', 'gpt'], capture_output=True)
    if process.returncode != 0:
        shared_events.append(f'Failed to label {drive_name} drive as gpt: {process.stderr.decode()}')
    
    shared_events.append("label gpt: " + process.stdout.decode())
    
    process = subprocess.run(['parted', '/dev/' + drive_name, '--script', 'mkpart', 'bootloader', 'c12a7328-f81f-11d2-ba4b-00a0c93ec93b', '1MiB', '1024MiB'], capture_output=True)
    if process.returncode != 0:
        shared_events.append(f'Failed to make boot partition on {drive_name} drive: {process.stderr.decode()}')
    
    shared_events.append("mkpart 1: " + process.stdout.decode())
    
    process = subprocess.run(['parted', '/dev/' + drive_name, '--script', 'mkpart', 'primary', 'ext4', '1024MiB', '100%'], capture_output=True)
    if process.returncode != 0:
        shared_events.append(f'Failed to make main partition on {drive_name} drive: {process.stderr.decode()}')
    
    shared_events.append("mkpart 2: " + process.stdout.decode())
    
    # process = subprocess.run(['mkfs.fat', '-F', '32', '/dev/' + drive_name + '1'], capture_output=True)
    # if process.returncode != 0:
        # shared_events.append(f'Failed to format boot partition on {drive_name} drive: {process.stderr.decode()}')
    # 
    # shared_events.append(process.stdout.decode())
    # 
    # process = subprocess.run(['mkfs.ext4', '/dev/' + drive_name + '2'], capture_output=True)
    # if process.returncode != 0:
        # shared_events.append(f'Failed to format main partition on {drive_name} drive: {process.stderr.decode()}')
    # 
    # shared_events.append(process.stdout.decode())
    # 
    # process = subprocess.run(['parted', '/dev/' + drive_name, '--script', 'set', '1', 'boot', 'on'], capture_output=True)
    # if process.returncode != 0:
        # shared_events.append(f'Failed to make boot partition on {drive_name} drive bootable: {process.stderr.decode()}')
    # 
    # shared_events.append(process.stdout.decode())
    

def mount_fs(installation_object: InstallInfo, partition_name: str, destination: str):
    partition_device = '/dev/' + partition_name

    process = subprocess.run(['mount', partition_device, destination, '-m'], capture_output=True)
    if process.returncode != 0:
        shared_events.append(f'Failed to mount root partition: {process.stderr.decode()}')
        return False

    shared_events.append(f'Mounted {partition_name} partition to {destination}')

    return True