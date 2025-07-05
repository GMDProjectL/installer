from shared import shared_events
from process_utils import run_command, run_command_in_chroot
from permission_utils import fix_user_permissions


def sudo_wheel(root: str):
    shared_events.append(f'Uncommenting wheel for {root}...')

    with open(f'{root}/etc/sudoers', 'r') as file:
        lines = file.readlines()

    with open(f'{root}/etc/sudoers', 'w') as file:
        for line in lines:
            if '%wheel ALL=(ALL:ALL) ALL' in line:
                file.write(line.replace('#', '', 1).replace(') ALL', ') NOPASSWD:ALL'))
            else:
                file.write(line)
            file.write('\n')
    
    return True


def change_password(root: str, user: str, password: str):
    shared_events.append(f'Changing password for {user}...')
    
    result = run_command_in_chroot(root, [
        'sh', '-c', f'echo -e "{password}\n{password}" | passwd {user}'
    ])

    if result.returncode != 0:
        shared_events.append(f'Failed to change password for root: {result.stderr}')
        return False
    
    return True


def mkinitpcio(root: str):
    shared_events.append('Generating initramfs...')

    result = run_command_in_chroot(root, ['mkinitcpio', '-P'])
    
    if result.returncode != 0:
        shared_events.append(f'Failed to mkinitcpio: {result.stderr}')
        return False
    
    return True

def create_user(root: str, username: str, password: str):
    shared_events.append(f'Creating user {username}...')

    result = run_command_in_chroot(root, [
        'useradd', '-m', '-G',
        'wheel', '-s', '/bin/fish', username
    ])

    if result.returncode != 0:
        shared_events.append(f'Failed to create user: {result.stderr}')
        return False
    
    if not change_password(root, username, password):
        return False
    
    return True


def add_to_input(root: str, username: str):
    shared_events.append(f'Adding {username} to input group...')

    result = run_command_in_chroot(root, [
        'usermod', '-a', '-G',
        'input', username
    ])

    if result.returncode != 0:
        shared_events.append(f'Failed to add user to input group: {result.stderr}')
        return False
    
    return True


def activate_systemd_service(root: str, service: str, user: str = ''):
    shared_events.append(f'Activating {service}...')

    if user != '':
        default_target_wants = f'/home/{user}/.config/systemd/user/default.target.wants'
        run_command(['mkdir', '-p', root + default_target_wants])
        result = run_command_in_chroot(root, [
            'ln', '-s', f'/usr/lib/systemd/user/{service}.service', f'{default_target_wants}/{service}.service'
        ])
        
        if result.returncode != 0:
            shared_events.append(f'Failed to activate {service}: {result.stderr}')
            return False
        
        fix_user_permissions(root, user)
        
        return True

    result = run_command_in_chroot(root, ['systemctl', 'enable', service])
    
    if result.returncode != 0:
        shared_events.append(f'Failed to activate {service}: {result.stderr}')
        return False
    
    return True