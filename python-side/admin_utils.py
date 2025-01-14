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
            if '%wheel ALL=(ALL:ALL) ALL' in line:
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


def create_user(installation_object: InstallInfo, root: str):
    shared_events.append('Creating user...')
    user_name = installation_object.username
    password = installation_object.password

    result = os.system(f'arch-chroot {root} useradd -m -G wheel -s /bin/bash {user_name}')

    if result != 0:
        shared_events.append('Failed to create user')
        return False
    
    if not change_password(installation_object, root, user_name, password):
        shared_events.append('Failed to set user password')
        return False
    
    return True