from gdltypes import InstallInfo
from shared import shared_events
from copy import deepcopy
from disk_utils import mount_fs, format_fs, clear_mountpoints, nuke_drive
from pacman_utils import pacstrap, pacman_install, enable_multilib, connect_chaotic_aur
from admin_utils import sudo_wheel, change_password, create_user, add_to_input
from grub_utils import install_grub, update_grub, patch_default_grub
from proprietary_drivers_utils import try_install_broadcom, try_install_nvidia
from oobe_utils import adjust_permissions, clone_oobe, create_oobe_autostart, install_oobe_dependencies
from misc_utils import (
    activate_systemd_service, generate_fstab, generate_locales, generate_localtime, 
    patch_distro_release, install_gdl_xdg_icon, patch_sddm_theme, copy_kde_config,
    install_plymouth
)


def failmsg():
    shared_events.append(f'Fatal error. Installation failed.')


def start_installation(installation_object: InstallInfo):
    debug_inso = deepcopy(installation_object)

    debug_inso.password = '*' * len(installation_object.password)
    debug_inso.password2 = '*' * len(installation_object.password2)

    print("Installing things:", debug_inso)
    shared_events.append(f'Installation started. Received installation object: {debug_inso}')

    if installation_object.method == 'nuke-drive':
        nuke_drive(installation_object, installation_object.selectedDrive)
    
    installation_root = '/mnt/installation'
    installation_boot = installation_root + '/boot/efi'

    clear_mountpoints(installation_object, installation_root)
    
    if not format_fs(installation_object, installation_object.rootPartition, installation_root):
        failmsg()
        return

    if not mount_fs(installation_object, installation_object.rootPartition, installation_root):
        failmsg()
        return

    if installation_object.formatBootPartition:
        if not format_fs(installation_object, installation_object.bootPartition, installation_boot, bootable=True):
            failmsg()
            return
    
    if not mount_fs(installation_object, installation_object.bootPartition, installation_boot):
        failmsg()
        return

    if not pacstrap(installation_boot, installation_root):
        failmsg()
        return

    fstab = generate_fstab(installation_object, installation_root)

    with open(f'{installation_root}/etc/fstab', 'w') as f:
        f.write(fstab)
    
    if not generate_localtime(installation_object, installation_root):
        failmsg()
        return
    
    if not generate_locales(
            installation_object, 
            installation_root, 
            ["en_US.UTF-8", "ru_RU.UTF-8"]
        ):
        failmsg()
        return
    
    system_locale = "en_US.UTF-8"

    if installation_object.language == 'ru':
        system_locale = "ru_RU.UTF-8"
    
    with open(f'{installation_root}/etc/locale.conf', 'w') as f:
        f.write(f"LANG={system_locale}\n")
    
    with open(f'{installation_root}/etc/hostname', 'w') as f:
        f.write(installation_object.computerName)
    
    if not change_password(installation_object, installation_root, 'root', installation_object.password):
        failmsg()
        return
    
    if not connect_chaotic_aur(installation_object, installation_root):
        failmsg()
        return
    
    de_packages = []

    if installation_object.de == "gnome":
        de_packages = [
            "gdm", "gnome", "gnome-tweaks", 
            "gnome-photos", "dconf", "dconf-editor",
            "adw-gtk-theme"
        ]
    
    if installation_object.de == "kde":
        de_packages = [
            "plasma", "sddm", "ark", "dolphin",
            "konsole", "kio-admin", "gwenview", "kate",
            "breeze5", "spectacle"
        ]
    
    if not pacman_install(
            installation_object, 
            installation_root, 
            [
                "grub", "efibootmgr", 
                "electron33", "nodejs", "npm",
                "pamac", "apple-fonts", "yay",
                "p7zip", 
                "zip", "unzip", "unrar", "neofetch",
                "sof-firmware"
            ] + de_packages
        ):
        failmsg()
        return
    
    if not create_user(installation_object, installation_root):
        failmsg()
        return
    
    if not sudo_wheel(installation_object, installation_root):
        failmsg()
        return
    
    if installation_object.de == 'kde':
        if not activate_systemd_service(installation_object, installation_root, "sddm.service"):
            failmsg()
            return
    
    if installation_object.de == 'gnome':
        if not activate_systemd_service(installation_object, installation_root, "gdm.service"):
            failmsg()
            return
    
    activate_systemd_service(installation_object, installation_root, "NetworkManager")
    
    try_install_nvidia(installation_object, installation_root)

    try_install_broadcom(installation_object, installation_root)

    patch_distro_release(installation_object, installation_root)
    
    if not install_grub(installation_object, installation_root):
        failmsg()
        return
    
    patch_default_grub(installation_object, installation_root)

    update_grub(installation_object, installation_root)

    patch_sddm_theme(installation_object, installation_root)

    install_gdl_xdg_icon(installation_object, installation_root)

    if installation_object.enableMultilibRepo:
        enable_multilib(installation_root)

        if installation_object.installSteam:
            if installation_object.vulkanNvidia:
                pacman_install(installation_object, installation_root, [
                    "lib32-nvidia-utils",
                    "nvidia-utils"
                ])
            
            if installation_object.vulkanAmd:
                pacman_install(installation_object, installation_root, [
                    "lib32-amdvlk",
                    "amdvlk",
                    "lib32-vulkan-radeon",
                    "vulkan-radeon"
                ])
            
            if installation_object.vulkanIntel:
                pacman_install(installation_object, installation_root, [
                    "lib32-vulkan-intel",
                    "vulkan-intel"
                ])
            
            pacman_install(installation_object, installation_root, [
                "steam"
            ])
        
        if installation_object.installWine:
            pacman_install(installation_object, installation_root, [
                "wine"
            ])

            if installation_object.installWinetricks:
                pacman_install(installation_object, installation_root, [
                    "winetricks"
                ])
        
    if installation_object.installGnomeDisks:
        pacman_install(installation_object, installation_root, [
            "gnome-disk-utility"
        ])
    
    if installation_object.installIntelMedia:
        pacman_install(installation_object, installation_root, [
            "intel-media-driver",
            "intel-media-sdk"
        ])
    
    shared_events.append('Setting up default KDE settings...')

    copy_kde_config(installation_object, installation_root)
    install_plymouth(installation_object, installation_root)
    add_to_input(installation_object, installation_root)

    if installation_object.setupBluetooth:
        pacman_install(installation_object, installation_root, [
            "bluez"
        ])
        activate_systemd_service(installation_object, installation_root, "bluetooth.service")
    
    if not clone_oobe(installation_object, installation_root):
        failmsg()
        return
    
    if not adjust_permissions(installation_object, installation_root):
        failmsg()
        return
    
    if not install_oobe_dependencies(installation_object, installation_root):
        failmsg()
        return
    
    if not adjust_permissions(installation_object, installation_root):
        failmsg()
        return
    
    create_oobe_autostart(installation_object, installation_root)
    
    shared_events.append('Project GDL Installed!')
