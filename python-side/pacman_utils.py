import os
from gdltypes import InstallInfo
from shared import shared_events
import subprocess


def append_mirrorlist(root: str):
    with open(root + '/etc/pacman.conf', 'a') as f:
        f.write('''
[chaotic-aur]
Include = /etc/pacman.d/chaotic-mirrorlist''')


def enable_multilib(root: str):
    with open(root + '/etc/pacman.conf', 'r') as f:
        pacman_conf = f.read()

    pacman_conf = pacman_conf.replace('#[multilib]\n#Include', '[multilib]\nInclude')

    with open(root + '/etc/pacman.conf', 'w') as f:
        f.write(pacman_conf)


def connect_chaotic_aur(installation_object: InstallInfo, root: str):
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

    update_result = os.system(f"arch-chroot {root} sudo pacman --noconfirm -Syyuu")

    shared_events.append('Installed Chaotic AUR!')

    return True


def pacstrap(installation_object: InstallInfo, destination: str):
    process = subprocess.Popen([
        'pacstrap',
        '-K', destination,
        'base', 'base-devel', 'linux', 'linux-firmware', 
        'linux-headers', 'dkms', 'vim', 'networkmanager',
        'nano', 'firefox', 'sudo'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, universal_newlines=True)
    
    for line in iter(process.stdout.readline, ''):
        shared_events.append(f'Pacstrapping: {line.strip()}')
    process.wait()
    
    if process.returncode != 0:
        for line in iter(process.stderr.readline, ''):
            shared_events.append(f'Failed to pacstrap: {line.strip()}')
        
        return False
    
    return True


def pacman_install(installation_object: InstallInfo, destination: str, packages: list):
    process = subprocess.Popen([
        'arch-chroot', destination,
        'pacman', '-Syu', *packages, '--noconfirm', '--noprogressbar', '--needed'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, universal_newlines=True)
    
    for line in iter(process.stdout.readline, ''):
        shared_events.append(f'Installing: {line.strip()}')
    process.wait()
    
    if process.returncode != 0:
        for line in iter(process.stderr.readline, ''):
            shared_events.append(f'Failed to install: {line.strip()}')
        
        return False
    
    return True


def pacman_install_from_file(installation_object: InstallInfo, destination: str, filename: str):
    process = subprocess.Popen([
        'arch-chroot', destination,
        'pacman', '-U', filename, '--noconfirm', '--noprogressbar', '--needed'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, universal_newlines=True)
    
    for line in iter(process.stdout.readline, ''):
        shared_events.append(f'Installing: {line.strip()}')
    process.wait()
    
    if process.returncode != 0:
        for line in iter(process.stderr.readline, ''):
            shared_events.append(f'Failed to install: {line.strip()}')
        
        return False
    
    return True