import os
from gdltypes import InstallInfo
from shared import shared_events
from copy import deepcopy
import time
import subprocess


def clear_mountpoints(installation_object: InstallInfo, root: str):
    shared_events.append(f'Unmounting {root} just in case...')

    process = subprocess.run(['umount', '-Rlf', root], capture_output=True)
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


def generate_fstab(installation_object: InstallInfo, destination: str):
    shared_events.append(f'Generating fstab for {destination}')

    process = subprocess.run(['genfstab', '-U', destination], capture_output=True)
    fstab = process.stdout.decode()

    shared_events.append(f'Generated fstab for {destination}: {fstab}')

    return fstab


def generate_localtime(installation_object: InstallInfo, root: str):
    shared_events.append(f'Linking zoneinfo for {root}...')

    process = subprocess.run([
        'arch-chroot', root, 
        'ln', '-sf', ('/usr/share/zoneinfo/' 
        + f'{installation_object.timezoneRegion}/{installation_object.timezoneInfo}'), 
        '/etc/localtime'
    ], capture_output=True)

    if process.returncode != 0:
        shared_events.append(f'Failed to link zoneinfo for {root}: {process.stderr.decode()}')
        return False
    
    return True


def generate_locales(installation_object: InstallInfo, root: str, locales: list):
    shared_events.append(f'Uncommenting locales for {root}...')

    with open(f'{root}/etc/locale.gen', 'r') as file:
        lines = file.readlines()

    with open(f'{root}/etc/locale.gen', 'w') as file:
        for line in lines:
            if any(locale in line for locale in locales):
                file.write(line.replace('#', '', 1))
            else:
                file.write(line)
            file.write('\n')

    process = subprocess.run([
        'arch-chroot', root, 
        'locale-gen'
    ], capture_output=True)

    if process.returncode != 0:
        shared_events.append(f'Failed to generate locales for {root}: {process.stderr.decode()}')
        return False
    
    return True


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


def activate_systemd_service(installation_object: InstallInfo, destination: str, service: str):
    shared_events.append(f'Activating {service}...')

    process = subprocess.run([
        'arch-chroot', destination,
        'systemctl', 'enable', service
        ], capture_output=True)
    
    if process.returncode != 0:
        shared_events.append(f'Failed to activate {service}: {process.stderr.decode()}')
        return False
    
    return True


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


def append_mirrorlist(root: str):
    with open(root + '/etc/pacman.conf', 'a') as f:
        f.write('''
[chaotic-aur]
Include = /etc/pacman.d/chaotic-mirrorlist''')


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


def get_lspci(installation_object: InstallInfo):
    '''lspci -k
    '''
    process = subprocess.run(['lspci', '-k'], capture_output=True)
    lspci = process.stdout.decode()

    return lspci


def is_nouveau(installation_object: InstallInfo):
    lspci = get_lspci(installation_object)
    if 'in use: nouveau' in lspci:
        return True
    
    return False


def is_nvidia(installation_object: InstallInfo):
    lspci = get_lspci(installation_object)
    if 'in use: nvidia' in lspci:
        return True
    
    return False


def try_install_nvidia(installation_object: InstallInfo, root: str):
    if not is_nvidia(installation_object) and not is_nouveau(installation_object):
        shared_events.append('Your system doesn\'t have NVIDIA GPU. Skipping.')
        return
    
    shared_events.append('Installing NVIDIA drivers...')
    result = pacman_install(installation_object, root, ['nvidia-dkms', 'nvidia-utils', 'nvidia-settings'])

    if not result:
        shared_events.append('Failed to install NVIDIA drivers')


def patch_distro_release(installation_object: InstallInfo, root: str):
    shared_events.append('Patching distro release...')
    # changing /usr/lib/os-release
    with open(root + '/usr/lib/os-release', 'r') as f:
        content = f.read()
        content = content.replace("Arch Linux", "Project GDL (Arch Linux)")
        content = content.replace("ID=arch", "ID=projectgdl")
        content = content.replace('HOME_URL="https://archlinux.org/"', 'HOME_URL="https://t.me/ProjectGDL"')
        content = content.replace('BUG_REPORT_URL="https://bugs.archlinux.org/"', 'BUG_REPORT_URL="https://t.me/ProjectGDL"')
        content = content.replace('DOCUMENTATION_URL="https://wiki.archlinux.org/"', 'DOCUMENTATION_URL="https://t.me/ProjectGDL"')
        content = content.replace('SUPPORT_URL="https://bbs.archlinux.org/"', 'SUPPORT_URL="https://t.me/ProjectGDL"')
        content = content.replace(
            'BUG_REPORT_URL="https://gitlab.archlinux.org/groups/archlinux/-/issues"', 
            'BUG_REPORT_URL="https://t.me/ProjectGDL"'
        )
        content = content.replace(
            'archlinux-logo', 
            'projectgdl-logo'
        )
    
    with open(root + '/usr/lib/os-release', 'w') as f:
        f.write(content)


def patch_default_grub(installation_object: InstallInfo, root: str):
    shared_events.append('Patching default grub...')

    pacman_install(installation_object, root, ['os-prober', 'grub-theme-vimix'])

    # changing /etc/default/grub
    with open(root + '/etc/default/grub', 'r') as f:
        content = f.read()
        content = content.replace('GRUB_DISTRIBUTOR="Arch"', 'GRUB_DISTRIBUTOR="ProjectGDL"')
        content = content.replace('#GRUB_THEME="/path/to/gfxtheme"', 'GRUB_THEME="/usr/share/grub/themes/Vimix/theme.txt"')
        content = content.replace('#GRUB_DISABLE_OS_PROBER=false', 'GRUB_DISABLE_OS_PROBER=false"')
    
    with open(root + '/etc/default/grub', 'w') as f:
        f.write(content)


def start_installation(installation_object: InstallInfo):
    debug_inso = deepcopy(installation_object)

    debug_inso.password = '*' * len(installation_object.password)
    debug_inso.password2 = '*' * len(installation_object.password2)

    print("Installing things:", debug_inso)
    shared_events.append(f'Installation started. Received installation object: {debug_inso}')

    if installation_object.method == 'nuke-drive':
        shared_events.append(f'Nuking drive is unavailable right now. Please use a different method.')
        return
    
    installation_root = '/mnt/installation'
    installation_boot = installation_root + '/boot/efi'

    clear_mountpoints(installation_object, installation_root)
    
    if not format_fs(installation_object, installation_object.rootPartition, installation_root):
        return

    if not mount_fs(installation_object, installation_object.rootPartition, installation_root):
        return

    if installation_object.formatBootPartition:
        if not format_fs(installation_object, installation_object.bootPartition, installation_boot, bootable=True):
            return
    
    if not mount_fs(installation_object, installation_object.bootPartition, installation_boot):
        return

    if not pacstrap(installation_boot, installation_root):
        return

    fstab = generate_fstab(installation_object, installation_root)

    with open(f'{installation_root}/etc/fstab', 'w') as f:
        f.write(fstab)
    
    if not generate_localtime(installation_object, installation_root):
        return
    
    if not generate_locales(
            installation_object, 
            installation_root, 
            ["en_US.UTF-8", "ru_RU.UTF-8"]
        ):
        return
    
    system_locale = "en_US.UTF-8"

    if installation_object.language == 'ru':
        system_locale = "ru_RU.UTF-8"
    
    with open(f'{installation_root}/etc/locale.conf', 'w') as f:
        f.write(f"LANG={system_locale}\n")
    
    with open(f'{installation_root}/etc/hostname', 'w') as f:
        f.write(installation_object.computerName)
    
    if not change_password(installation_object, installation_root, 'root', installation_object.password):
        return
    
    if not connect_chaotic_aur(installation_object, installation_root):
        return
    
    if not pacman_install(
            installation_object, 
            installation_root, 
            [
                "plasma", "sddm", 
                "grub", "efibootmgr", 
                "electron33", "nodejs", "npm",
                "pamac", "apple-fonts", "yay",
                "konsole", "dolphin", "kio-admin"
            ]
        ):
        return
    
    if not create_user(installation_object, installation_root):
        return
    
    if not sudo_wheel(installation_object, installation_root):
        return
    
    if not activate_systemd_service(installation_object, installation_root, "sddm.service"):
        return
    
    try_install_nvidia(installation_object, installation_root)

    patch_distro_release(installation_object, installation_root)
    
    if not install_grub(installation_object, installation_root):
        return
    
    patch_default_grub(installation_object, installation_root)

    update_grub(installation_object, installation_root)
    
    shared_events.append('Project GDL Installed!')