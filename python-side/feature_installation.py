from gdltypes import UpdateFlags
from utils import failmsg
from shared import shared_progress, shared_events

from base.pacman import pacman_install, pacman_remove, enable_multilib, make_pacman_more_fun, blacklist_package
from base.admin import activate_systemd_service, install_nopasswd_pkrule
from base.grub import patch_default_grub, update_grub
from base.system_configs import install_sayodevice_udev_rule, copy_sysctl_config
from cosmetic.distro_release import patch_distro_release
from cosmetic.sddm import patch_sddm_theme
from cosmetic.branding import install_gdl_xdg_icon
from cosmetic.lact import fix_lact_appearance
from cosmetic.misc import copy_kde_config, copy_fastfetch_config, copy_hidden_apps
from cosmetic.plymouth import install_plymouth
from cosmetic.fish import copy_fish_config
from cosmetic.konsole import copy_konsole_config
from apps.proprietary_drivers import try_install_broadcom, try_install_nvidia, copy_nvidia_prime_steam
from apps.oobe import clone_oobe, adjust_oobe_permissions, install_oobe_dependencies, create_oobe_autostart
from apps.hiddify import install_hiddify
from apps.spectacle import install_spectacle_fix
from apps.gsr import install_gsrn, install_gsrui, copy_gsr_handler_stuff
from apps.geode import install_geode_installer
from apps.gdl_updater import install_gdl_updater
from apps.aptpac import install_aptpac


def install_features(root: str, update_flags: UpdateFlags):
    de_packages = []

    if update_flags.de == "gnome":
        de_packages = [
            "gdm", "gnome", "gnome-tweaks", 
            "gnome-photos", "dconf", "dconf-editor"
        ]
    
    if update_flags.de == "kde":
        de_packages = [
            "plasma", "sddm", "ark", "dolphin", "kwin-effect-rounded-corners-git",
            "konsole", "kio-admin", "gwenview", "kate", "plasma5-integration",
            "breeze5", "spectacle", "packagekit-qt6", "flatpak-kcm"
        ]
    
    if not pacman_install(
            root, 
            [
                "electron34", "nodejs", "npm",
                "pnpm", "base-devel", "python-dbus", "python-pyudev", "python-gobject",
                "pamac", "adwaita-fonts", "yay",
                "7zip", "zip", "unzip", "unrar",
                "fastfetch", "gpu-screen-recorder-gtk",
                "sof-firmware", "fastfetch", "btop", "adw-gtk-theme",
                "noto-fonts", "noto-fonts-emoji", "noto-fonts-cjk"
            ] + de_packages
        ):
        failmsg()
        return
    
    shared_progress.append('Done DE')

    install_aptpac(root)
    
    if update_flags.de == 'kde':
        if not activate_systemd_service(root, "sddm.service"):
            failmsg()
            return
    
    if update_flags.de == 'gnome':
        if not activate_systemd_service(root, "gdm.service"):
            failmsg()
            return
        
    shared_progress.append('Done DM')
    
    activate_systemd_service(root, "NetworkManager")

    shared_progress.append('Done Network')

    if update_flags.setupCachyosKernel:
        if not pacman_install(root, ["linux-cachyos-lts", "linux-cachyos-lts-headers"]):
            failmsg()
            return
        
        pacman_remove(root, ["linux", "linux-headers"])
        pacman_remove(root, ["linux-lts", "linux-lts-headers"])
        
        shared_progress.append('CachyOS Kernel installed')
        
    
    try_install_nvidia(root)

    try_install_broadcom(root)

    shared_progress.append('Done proprietary')

    if not update_flags.dontUpdateGrub:
        patch_distro_release(root)
        patch_default_grub(root, update_flags.doOsProber)
        update_grub(root)
        
        shared_progress.append('Done GRUB')

    patch_sddm_theme(root)

    shared_progress.append('Done SDDM')

    install_gdl_xdg_icon(root)

    shared_progress.append('Done Branding')

    if pacman_install(root, ["power-profiles-daemon"]):
        activate_systemd_service(root, "power-profiles-daemon")

    shared_progress.append('Done Power')

    if update_flags.enableMultilibRepo:
        enable_multilib(root)

        if update_flags.installSteam:
            if update_flags.vulkanNvidia:
                pacman_install(root, ["lib32-nvidia-utils", "nvidia-utils"])
            
            if update_flags.vulkanAmd:
                pacman_install(root, [
                    "lib32-amdvlk", "amdvlk",
                    "lib32-vulkan-radeon", "vulkan-radeon"
                ])
            
            if update_flags.vulkanIntel:
                pacman_install(root, ["lib32-vulkan-intel", "vulkan-intel"])
            
            pacman_install(root, ["steam"])

            if update_flags.vulkanNvidia:
                copy_nvidia_prime_steam(root)
        
        if update_flags.installWine:
            pacman_install(root, ["wine"])

            if update_flags.installWinetricks:
                pacman_install(root, ["winetricks"])

    shared_progress.append('Done Multilib')
        
    if update_flags.installGnomeDisks:
        pacman_install(root, ["gnome-disk-utility"])
    
    if update_flags.installIntelMedia:
        pacman_install(root, ["intel-media-driver", "intel-media-sdk"])
    
    if update_flags.installLact:
        if not pacman_install(root, ["lact"]):
            failmsg()
            return

        activate_systemd_service(root, "lactd")
        fix_lact_appearance(root, update_flags.username)

    shared_progress.append('Done Additional software')
    
    shared_events.append('Setting up default KDE settings...')

    if not update_flags.dontCopyKde:
        copy_kde_config(root, update_flags.username)

    copy_hidden_apps(root, update_flags.username)

    install_plymouth(root, update_flags.fromUpdate)

    if update_flags.setupBluetooth:
        pacman_install(root, ["bluez"])
        activate_systemd_service(root, "bluetooth.service")
    
    shared_progress.append('Done BT')

    if not update_flags.fromUpdate:
        if not clone_oobe(root):
            failmsg()
            return
        
        shared_progress.append('Done OOBE')
        
        if not adjust_oobe_permissions(root):
            failmsg()
            return
        
        shared_progress.append('Done Perms')
        
        if not install_oobe_dependencies(root):
            failmsg()
            return
        
        shared_progress.append('Done Deps')
        
        if not adjust_oobe_permissions(root):
            failmsg()
            return
        
        shared_progress.append('Done Perms')
        
        create_oobe_autostart(root, update_flags.username)

    install_sayodevice_udev_rule(root)
    install_nopasswd_pkrule(root)
    copy_sysctl_config(root)
    install_hiddify(root)
    install_gdl_updater(root)

    shared_progress.append('Done udev, polkit, sysctl and hiddify, fixed spectacle.')

    if update_flags.de == 'kde':
        pacman_remove(root, ['plasma-welcome'])

        blacklist_package(root, 'gpu-screen-recorder-notification-git')
        blacklist_package(root, 'gpu-screen-recorder-ui-git')

        if not install_gsrn(root):
            failmsg()
            return
        
        if not install_gsrui(root):
            failmsg()
            return
        
        if not activate_systemd_service(root, 'gpu-screen-recorder-ui', update_flags.username):
            failmsg()
            return
        
        if not copy_gsr_handler_stuff(root, update_flags.username):
            failmsg()
            return
        
        install_spectacle_fix(root, update_flags.username)

        if not update_flags.dontCopyKde:
            copy_konsole_config(root, update_flags.username)

    copy_fastfetch_config(root, update_flags.username)
    copy_fish_config(root, update_flags.username)
    make_pacman_more_fun(root)

    shared_progress.append('Done Terminal Ricing')

    install_geode_installer(root)

    shared_progress.append('Done Geode')