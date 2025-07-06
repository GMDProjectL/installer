import os
from shared import shared_events
from process_utils import run_command_in_chroot, run_command
from patching_utils import replace_str_in_file


def append_mirrorlist(root: str):
    with open(root + '/etc/pacman.conf', 'a') as f:
        f.write('''
[chaotic-aur]
Include = /etc/pacman.d/chaotic-mirrorlist''')


def enable_multilib(root: str):
    shared_events.append('Enabling multilib repository...')

    replace_str_in_file(root + '/etc/pacman.conf', '#[multilib]\n#Include', '[multilib]\nInclude')


def make_pacman_more_fun(root: str):
    shared_events.append('Making pacman more fun...')

    replace_str_in_file(root + '/etc/pacman.conf', '#Color', 'Color\nILoveCandy')


def make_pacman_more_unsafe(root: str):
    shared_events.append('Disabling signature checking...')

    replace_str_in_file(root + '/etc/pacman.conf', 'Required DatabaseOptional', 'Never')


def run_reflector(root: str = '', country: str = ''):
    shared_events.append('Running reflector to update mirrorlist...')

    if country == '':
        command = ['reflector', '--latest', '5', '--sort', 'rate', '--save', '/etc/pacman.d/mirrorlist']
    else:
        command = ['reflector', '--country', country, '--latest', '5', '--sort', 'rate', '--save', '/etc/pacman.d/mirrorlist']
    
    result = run_command(command)
    
    if result.returncode != 0:
        shared_events.append(f'Failed to run reflector: {result.stderr}')
        return False
    
    return True


def connect_chaotic_aur(root: str):
    shared_events.append('Installing Chaotic AUR...')

    CHAOTIC_AUR_KEY = '3056513887B78AEB'
    recv_result = os.system(f'arch-chroot {root} pacman-key --recv-key {CHAOTIC_AUR_KEY} --keyserver keyserver.ubuntu.com')
    
    if recv_result != 0:
        shared_events.append('Failed to connect to Chaotic AUR')
        return False

    lsign_result = os.system(f'arch-chroot {root} pacman-key --lsign-key {CHAOTIC_AUR_KEY}')
    
    if lsign_result != 0:
        shared_events.append('Failed to sign Chaotic AUR key')
        return False
    
    keyring_result = os.system(f"arch-chroot {root} pacman -U --noconfirm 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-keyring.pkg.tar.zst'")
    
    if keyring_result != 0:
        shared_events.append('Failed to install Chaotic AUR keyring')
        return False
    
    mirrorlist_result = os.system(f"arch-chroot {root} pacman -U --noconfirm 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-mirrorlist.pkg.tar.zst'")

    if mirrorlist_result != 0:
        shared_events.append('Failed to install Chaotic AUR mirrorlist')
        return False

    append_mirrorlist(root)

    run_command_in_chroot(root, ['pacman', '-Syyuu', '--noconfirm'])

    shared_events.append('Installed Chaotic AUR!')

    return True


def pacstrap(root: str):
    shared_events.append('Starting pacstrap...')
    result = run_command([
        'pacstrap', '-K', root, 
        'base', 'base-devel', 
        'linux', 'linux-firmware', 'linux-headers', 'dkms', 
        'vim', 'nano', 'sudo', 'fish', 
        'networkmanager', 'firefox'
    ])
    
    if result.returncode != 0:
        shared_events.append(f'Failed to run pacstrap: {result.stderr}')
        return False
    
    return True


def pacman_install(root: str, packages: list):
    shared_events.append(f'Installing packages: {", ".join(packages)}')

    result = run_command_in_chroot(root, ['pacman', '-Syu', *packages, '--noconfirm', '--noprogressbar', '--needed'])
    
    if result.returncode != 0:
        shared_events.append(f'Failed to install packages: {result.stderr}')
        return False
    
    return True


def pacman_remove(root: str, packages: list):
    shared_events.append(f'Removing packages: {", ".join(packages)}')

    result = run_command_in_chroot(root, ['pacman', '-R', '--noconfirm', '--noprogressbar', *packages])
    
    if result.returncode != 0:
        shared_events.append(f'Failed to remove packages: {result.stderr}')
        return False
    return True


def pacman_install_from_file(root: str, filename: str):
    shared_events.append(f'Installing from file: {filename}')

    result = run_command(['arch-chroot', root, 'pacman', '-U', filename, '--noconfirm', '--noprogressbar', '--needed'])
    
    if result.returncode != 0:
        shared_events.append(f'Failed to install from file: {result.stderr}')
        return False
    
    return True