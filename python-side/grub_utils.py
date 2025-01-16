from gdltypes import InstallInfo
from shared import shared_events
from pacman_utils import pacman_install
import os
import subprocess
import shutil


def update_grub(installation_object: InstallInfo, destination: str):
    shared_events.append('Generating GRUB config...')

    process = subprocess.Popen([
        'arch-chroot', destination,
        'grub-mkconfig',
        f'-o', '/boot/grub/grub.cfg'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, universal_newlines=True)
    
    for line in iter(process.stdout.readline, ''):
        shared_events.append(f'Generating: {line.strip()}')
    process.wait()
    
    if process.returncode != 0:
        for line in iter(process.stderr.readline, ''):
            shared_events.append(f'Failed to generate: {line.strip()}')
        
        return False
    
    shared_events.append('Installed GRUB successfully!')
    return True


def install_grub(installation_object: InstallInfo, destination: str):
    shared_events.append('Installing GRUB...')

    process = subprocess.Popen([
        'arch-chroot', destination,
        'grub-install',
        f'--efi-directory=/boot/efi', '--bootloader-id=ProjectGDL'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, universal_newlines=True)
    
    for line in iter(process.stdout.readline, ''):
        shared_events.append(f'Installing: {line.strip()}')
    process.wait()
    
    if process.returncode != 0:
        for line in iter(process.stderr.readline, ''):
            shared_events.append(f'Failed to install: {line.strip()}')
        
        return False

    update_grub(installation_object, destination)
    
    return True


def patch_default_grub(installation_object: InstallInfo, root: str):
    shared_events.append('Patching default grub...')

    pacman_install(installation_object, root, ['os-prober', 'grub-theme-vimix'])

    if not os.path.exists(root + '/usr/share/gdlbg'):
        os.makedirs(root + '/usr/share/gdlbg')
    

    script_dir = os.path.dirname(os.path.abspath(__file__))
    shutil.copy(script_dir + '/resources/.config/pgd-bg.png', root + '/usr/share/gdlbg/pgd-bg.png')

    # changing /etc/default/grub
    with open(root + '/etc/default/grub', 'r') as f:
        content = f.read()
        content = content.replace('GRUB_DISTRIBUTOR="Arch"', 'GRUB_DISTRIBUTOR="ProjectGDL"')
        content = content.replace('loglevel=3 quiet', 'loglevel=3 quiet splash')
        content = content.replace('#GRUB_BACKGROUND="/path/to/wallpaper"', 'GRUB_BACKGROUND="/usr/share/gdlbg/pgd-bg.png"')
        content = content.replace('#GRUB_DISABLE_OS_PROBER=false', 'GRUB_DISABLE_OS_PROBER=false')
        content = content.replace('GRUB_GFXMODE=auto', 'GRUB_GFXMODE=1920x1080')
    
    with open(root + '/etc/default/grub', 'w') as f:
        f.write(content)