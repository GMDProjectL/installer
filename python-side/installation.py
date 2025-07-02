from gdltypes import InstallInfo
from shared import shared_events, shared_progress
from copy import deepcopy
from disk_utils import mount_fs, format_fs, clear_mountpoints, nuke_drive
from pacman_utils import pacstrap, pacman_install, enable_multilib, connect_chaotic_aur, run_reflector
from admin_utils import sudo_wheel, change_password, create_user, add_to_input
from grub_utils import install_grub, update_grub, patch_default_grub
from proprietary_drivers_utils import try_install_broadcom, try_install_nvidia
from oobe_utils import adjust_permissions, clone_oobe, create_oobe_autostart, install_oobe_dependencies
from misc_utils import (
    activate_systemd_service, copy_nvidia_prime_steam, generate_fstab, generate_locales, generate_localtime, install_nopasswd_pkrule, 
    patch_distro_release, install_gdl_xdg_icon, patch_sddm_theme, copy_kde_config,
    install_plymouth, install_sayodevice_udev_rule, copy_sysctl_config, install_geode_installer
)
from hiddify_utils import install_hiddify


def failmsg():
    shared_events.append(f'Fatal error. Installation failed.')


# 30 STEPS IN THIS TIME. 15:50 2025-04-05
def start_installation(installation_object: InstallInfo):
    debug_inso = deepcopy(installation_object)

    debug_inso.password = '*' * len(installation_object.password)
    debug_inso.password2 = '*' * len(installation_object.password2)

    print("Installing things:", debug_inso)
    shared_events.append(f'Installation started. Received installation object: {debug_inso}')

    if installation_object.method == 'nuke-drive':
        nuke_drive(installation_object, installation_object.selectedDrive)
    
    shared_progress.append('Done nuking');
    
    installation_root = '/mnt/installation'
    installation_boot = installation_root + '/boot/efi'

    clear_mountpoints(installation_object, installation_root)
    
    if not format_fs(installation_object, installation_object.rootPartition, installation_root):
        failmsg()
        return
    
    shared_progress.append('Done formatting root');

    if not mount_fs(installation_object, installation_object.rootPartition, installation_root):
        failmsg()
        return
    
    shared_progress.append('Done mounting root');

    if installation_object.formatBootPartition:
        if not format_fs(installation_object, installation_object.bootPartition, installation_boot, bootable=True):
            failmsg()
            return
        
    shared_progress.append('Done formatting (or not) the boot partition');
    
    if not mount_fs(installation_object, installation_object.bootPartition, installation_boot):
        failmsg()
        return
    
    shared_progress.append('Done mounting the boot partition');

    shared_progress.append('Running mirror sorting...');
    
    if installation_object.runRussianReflector:
        run_reflector(country='Russia')
    else:
        run_reflector()
    shared_progress.append('Mirrors are sorted (probably)');
    

    if not pacstrap(installation_boot, installation_root):
        failmsg()
        return
    
    shared_progress.append('Done pacstrapping');

    fstab = generate_fstab(installation_object, installation_root)

    with open(f'{installation_root}/etc/fstab', 'w') as f:
        f.write(fstab)

    shared_progress.append('Done genfstab');
    
    if not generate_localtime(installation_object, installation_root):
        failmsg()
        return
    
    shared_progress.append('Done localtime');
    
    if not generate_locales(
            installation_object, 
            installation_root, 
            ["en_US.UTF-8", "ru_RU.UTF-8"]
        ):
        failmsg()
        
    
    system_locale = "en_US.UTF-8"

    if installation_object.language == 'ru':
        system_locale = "ru_RU.UTF-8"
    
    with open(f'{installation_root}/etc/locale.conf', 'w') as f:
        f.write(f"LANG={system_locale}\n")
        
    shared_progress.append('Done locales');
    
    with open(f'{installation_root}/etc/hostname', 'w') as f:
        f.write(installation_object.computerName)
    
    if not change_password(installation_object, installation_root, 'root', installation_object.password):
        failmsg()
        return
    
    shared_progress.append('Done root');
    
    if not connect_chaotic_aur(installation_object, installation_root):
        failmsg()
        return
    
    shared_progress.append('Done chaotic');
    
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
            "breeze5", "spectacle", "packagekit-qt6", "flatpak-kcm"
        ]
    
    if not pacman_install(
            installation_object, 
            installation_root, 
            [
                "grub", "efibootmgr", 
                "electron34", "nodejs", "npm",
                "pnpm",
                "pamac", "adwaita-fonts", "yay",
                "p7zip", "zip", "unzip", "unrar", 
                "neofetch",
                "sof-firmware", "fastfetch", "btop", "aptpac"
            ] + de_packages
        ):
        failmsg()
        return
    
    shared_progress.append('Done DE');
    
    if not create_user(installation_object, installation_root):
        failmsg()
        return
    
    shared_progress.append('Done user');
    
    if not sudo_wheel(installation_object, installation_root):
        failmsg()
        return
    
    shared_progress.append('Done sudo');
    
    if installation_object.de == 'kde':
        if not activate_systemd_service(installation_object, installation_root, "sddm.service"):
            failmsg()
            return
    
    if installation_object.de == 'gnome':
        if not activate_systemd_service(installation_object, installation_root, "gdm.service"):
            failmsg()
            return
        
    shared_progress.append('Done DM');
    
    activate_systemd_service(installation_object, installation_root, "NetworkManager")

    shared_progress.append('Done Network');

    if installation_object.setupCachyosKernel:
        if not pacman_install(
                installation_object, 
                installation_root, 
                [
                    "linux-cachyos", "linux-cachyos-headers"
                ]
            ):
            failmsg()
            return
        
        shared_progress.append('CachyOS Kernel installed');
        
    
    try_install_nvidia(installation_object, installation_root)

    try_install_broadcom(installation_object, installation_root)

    shared_progress.append('Done proprietary');

    patch_distro_release(installation_object, installation_root)
    
    if not install_grub(installation_object, installation_root):
        failmsg()
        return
    
    patch_default_grub(installation_object, installation_root)

    update_grub(installation_object, installation_root)
    
    shared_progress.append('Done GRUB');

    patch_sddm_theme(installation_object, installation_root)

    shared_progress.append('Done SDDM');

    install_gdl_xdg_icon(installation_object, installation_root)

    shared_progress.append('Done Branding');

    if pacman_install(installation_object, installation_root, [
        "power-profiles-daemon"
    ]):
        activate_systemd_service(installation_object, installation_root, "power-profiles-daemon")

    shared_progress.append('Done Power');

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

            if installation_object.vulkanNvidia:
                copy_nvidia_prime_steam(installation_object, installation_root)
        
        if installation_object.installWine:
            pacman_install(installation_object, installation_root, [
                "wine"
            ])

            if installation_object.installWinetricks:
                pacman_install(installation_object, installation_root, [
                    "winetricks"
                ])

    shared_progress.append('Done Multilib');
        
    if installation_object.installGnomeDisks:
        pacman_install(installation_object, installation_root, [
            "gnome-disk-utility"
        ])
    
    if installation_object.installIntelMedia:
        pacman_install(installation_object, installation_root, [
            "intel-media-driver",
            "intel-media-sdk"
        ])

    shared_progress.append('Done Additional software');
    
    shared_events.append('Setting up default KDE settings...')

    copy_kde_config(installation_object, installation_root)
    install_plymouth(installation_object, installation_root)
    add_to_input(installation_object, installation_root)

    if installation_object.setupBluetooth:
        pacman_install(installation_object, installation_root, [
            "bluez"
        ])
        activate_systemd_service(installation_object, installation_root, "bluetooth.service")
    
    shared_progress.append('Done BT');

    if not clone_oobe(installation_object, installation_root):
        failmsg()
        return
    
    shared_progress.append('Done OOBE');
    
    if not adjust_permissions(installation_object, installation_root):
        failmsg()
        return
    
    shared_progress.append('Done Perms');
    
    if not install_oobe_dependencies(installation_object, installation_root):
        failmsg()
        return
    
    shared_progress.append('Done Deps');
    
    if not adjust_permissions(installation_object, installation_root):
        failmsg()
        return
    
    shared_progress.append('Done Perms');
    
    create_oobe_autostart(installation_object, installation_root)

    install_sayodevice_udev_rule(installation_object, installation_root)
    install_nopasswd_pkrule(installation_object, installation_root)
    copy_sysctl_config(installation_object, installation_root)
    install_hiddify(installation_object, installation_root)

    shared_progress.append('Done udev, polkit, sysctl and hiddify');

    install_geode_installer(installation_object, installation_root)

    shared_progress.append('Done Geode');
    
    shared_events.append('Project GDL Installed!')
