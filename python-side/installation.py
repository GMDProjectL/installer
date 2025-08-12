import traceback
from gdltypes import InstallInfo, UpdateFlags
from shared import shared_events, shared_progress
from copy import deepcopy
from base.disks import mount_fs, format_fs, clear_mountpoints, nuke_drive, generate_fstab
from base.pacman import make_pacman_more_unsafe, pacstrap, connect_cachyos, run_reflector
from base.admin import sudo_wheel, change_password, create_user, add_to_input, mkinitpcio
from base.grub import install_grub
from base.locale import generate_locales, generate_localtime
from utils import failmsg
from feature_installation import install_features
from base.nm_dbus import copy_saved_connections


# 30 STEPS IN THIS TIME. 15:50 2025-04-05
def start_installation(installation_object: InstallInfo):
    debug_inso = deepcopy(installation_object)

    debug_inso.password = '*' * len(installation_object.password)
    debug_inso.password2 = '*' * len(installation_object.password2)

    print("Installing things:", debug_inso)
    shared_events.append(f'Installation started. Received installation object: {debug_inso}')

    if installation_object.method == 'nuke-drive':
        nuke_drive(installation_object.selectedDrive)
    
    shared_progress.append('Done nuking')
    
    installation_root = '/mnt/installation'
    installation_boot = installation_root + '/boot/efi'

    clear_mountpoints(installation_root)
    
    if not format_fs(installation_object.rootPartition, installation_root):
        failmsg()
        return
    
    shared_progress.append('Done formatting root')

    if not mount_fs(installation_object.rootPartition, installation_root):
        failmsg()
        return
    
    shared_progress.append('Done mounting root')

    if installation_object.formatBootPartition:
        if not format_fs(installation_object.bootPartition, installation_boot, bootable=True):
            failmsg()
            return
        
    shared_progress.append('Done formatting (or not) the boot partition')
    
    if not mount_fs(installation_object.bootPartition, installation_boot):
        failmsg()
        return
    
    shared_progress.append('Done mounting the boot partition')

    shared_progress.append('Running mirror sorting...')
    
    if installation_object.runRussianReflector:
        run_reflector(country='Russia')
    else:
        run_reflector()
    shared_progress.append('Mirrors are sorted (probably)')
    

    if not pacstrap(installation_root):
        failmsg()
        return
    
    shared_progress.append('Done pacstrapping')

    make_pacman_more_unsafe(installation_root) # I'm sorry it will be removed in the future

    fstab = generate_fstab(installation_root)

    with open(f'{installation_root}/etc/fstab', 'w') as f:
        f.write(fstab)

    shared_progress.append('Done genfstab')
    
    if not generate_localtime(installation_root, installation_object.timezoneRegion, installation_object.timezoneInfo):
        failmsg()
        return
    
    shared_progress.append('Done localtime')
    
    if not generate_locales(installation_root, ["en_US.UTF-8", "ru_RU.UTF-8"]):
        failmsg()
        
    system_locale = "en_US.UTF-8"

    if installation_object.language == 'ru':
        system_locale = "ru_RU.UTF-8"
    

    with open(f'{installation_root}/etc/locale.conf', 'w') as f:
        f.write(f"LANG={system_locale}\n")
        
    shared_progress.append('Done locales')
    

    with open(f'{installation_root}/etc/hostname', 'w') as f:
        f.write(installation_object.computerName)
    
    if not change_password(installation_root, 'root', installation_object.password):
        failmsg()
        return
    
    shared_progress.append('Done root')
    
    if not create_user(installation_root, installation_object.username, installation_object.password):
        failmsg()
        return
    
    shared_progress.append('Done user')

    add_to_input(installation_root, installation_object.username)
    
    if not sudo_wheel(installation_root):
        failmsg()
        return
    
    shared_progress.append('Done sudo')

    
    if not connect_cachyos(installation_root):
        failmsg()
        return
    
    mkinitpcio(installation_root)
    
    shared_progress.append('Done CachyOS repos')
    
    if not install_grub(installation_root):
        failmsg()
        return
    
    update_flags = UpdateFlags(
        installation_object.de,
        installation_object.setupCachyosKernel,
        installation_object.enableMultilibRepo,
        installation_object.installSteam,
        installation_object.installWine,
        installation_object.installWinetricks,
        installation_object.vulkanNvidia,
        installation_object.vulkanAmd,
        installation_object.vulkanIntel,
        installation_object.installGnomeDisks,
        installation_object.installIntelMedia,
        installation_object.setupBluetooth,
        installation_object.runRussianReflector,
        installation_object.installLact,
        False,
        installation_object.username,
        installation_object.doOsProber,
        installation_object.installZapret,
        False, False
    )

    install_features(installation_root, update_flags)

    shared_events.append('Trying to copy NetworkManager connections')

    if copy_saved_connections(installation_root):
        shared_events.append('Successfully copied connections')
    else:
        shared_events.append('Failed to copy connections')
    
    shared_events.append('Project GDL Installed!')

def start_update_process(update_flags: UpdateFlags):
    install_features('/', update_flags)
    shared_events.append('Project GDL Installed!')


def start_safe_installation(installation_object: InstallInfo):
    try:
        start_installation(installation_object)
    except Exception as e:
        shared_events.append('An error occurred during installation: ' + traceback.format_exc())
        print(traceback.format_exc())
        failmsg()


def start_safe_update(update_flags: UpdateFlags):
    try:
        start_update_process(update_flags)
    except Exception as e:
        shared_events.append('An error occurred during installation: ' + traceback.format_exc())
        print(traceback.format_exc())
        failmsg()