import os
from gdltypes import InstallInfo
from shared import shared_events
import subprocess


def sudo_wheel(installation_object: InstallInfo, root: str):
    shared_events.append(f'Uncommenting wheel for {root}...')

    with open(f'{root}/etc/sudoers', 'r') as file:
        lines = file.readlines()

    with open(f'{root}/etc/sudoers', 'w') as file:
        for line in lines:
            if '%wheel ALL=(ALL:ALL) NOPASSWD:ALL' in line:
                file.write(line.replace('#', '', 1))
            else:
                file.write(line)
            file.write('\n')
    
    return True


def change_password(installation_object: InstallInfo, root: str, user: str, password: str):
    process = subprocess.run([
        'arch-chroot', root, 
        'sh', '-c', f'echo -e "{password}\n{password}" | (passwd {user})'
    ], capture_output=True)

    if process.returncode != 0:
        shared_events.append(f'Failed to change password for root: {process.stderr.decode()}')
        return False
    
    return True


def mkinitpcio(installation_object, root: str):
    shared_events.append('Generating CPIO...')

    process = subprocess.Popen([
        'arch-chroot', root,
        'mkinitcpio', '-P'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, universal_newlines=True)
    
    for line in iter(process.stdout.readline, ''):
        shared_events.append(f'mkinitcpio: {line.strip()}')
    process.wait()
    
    if process.returncode != 0:
        for line in iter(process.stderr.readline, ''):
            shared_events.append(f'Failed to mkinitcpio: {line.strip()}')
        
        return False
    
    return True

def create_user(installation_object: InstallInfo, root: str):
    shared_events.append('Creating user...')
    user_name = installation_object.username
    password = installation_object.password

    process = subprocess.run([
        'arch-chroot', root, 
        'useradd', '-m', '-G',
        'wheel', '-s', '/bin/bash', user_name
    ], capture_output=True)

    result = process.returncode

    if result != 0:
        shared_events.append(f'Failed to create user: {process.stdout.decode()}')
        return False
    
    if not change_password(installation_object, root, user_name, password):
        return False
    
    return True


def add_to_input(installation_object: InstallInfo, root: str):
    shared_events.append('Adding user to input group...')
    user_name = installation_object.username

    process = subprocess.run([
        'arch-chroot', root, 
        'usermod', '-a', '-G',
        'input', user_name
    ], capture_output=True)

    result = process.returncode

    if result != 0:
        shared_events.append(f'Failed to add user to input group: {process.stdout.decode()}')
        return False
    
    return True