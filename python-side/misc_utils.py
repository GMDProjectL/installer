import os
from shared import shared_events
from pacman_utils import pacman_install
from admin_utils import mkinitpcio
from process_utils import run_command_in_chroot
from patching_utils import add_mkinitcpio_hook, uncomment_line_in_file, replace_str_in_file
from path_utils import get_resources_path, get_user_applications_dir, get_user_autostart_dir, get_user_config_dir
from permission_utils import fix_user_permissions
from resources_utils import copy_from_resources, copytree_from_resources, copy_user_config_dir
from github_utils import install_latest_gh_package


def patch_distro_release(root: str):
    shared_events.append('Patching distro release...')

    distro_release_path = root + '/usr/lib/os-release'

    replace_str_in_file(distro_release_path, 'Arch Linux', 'Project GDL (Arch Linux)')
    replace_str_in_file(distro_release_path, 'ID=arch', 'ID=projectgdl')
    replace_str_in_file(distro_release_path, 'HOME_URL="https://archlinux.org/"', 'HOME_URL="https://t.me/ProjectGDL"')
    replace_str_in_file(distro_release_path, 'BUG_REPORT_URL="https://bugs.archlinux.org/"', 'BUG_REPORT_URL="https://t.me/ProjectGDL"')
    replace_str_in_file(distro_release_path, 'DOCUMENTATION_URL="https://wiki.archlinux.org/"', 'DOCUMENTATION_URL="https://t.me/ProjectGDL"')
    replace_str_in_file(distro_release_path, 'SUPPORT_URL="https://bbs.archlinux.org/"', 'SUPPORT_URL="https://t.me/ProjectGDL"')
    replace_str_in_file(distro_release_path, 
        'BUG_REPORT_URL="https://gitlab.archlinux.org/groups/archlinux/-/issues"', 
        'BUG_REPORT_URL="https://t.me/ProjectGDL"'
    )
    replace_str_in_file(distro_release_path, 'archlinux-logo', 'projectgdl-logo')


def patch_sddm_theme(root: str):
    shared_events.append('Patching default SDDM theme...')

    sddm_conf_dir = root + '/etc/sddm.conf.d'
    sddm_breeze_dir = root + '/usr/share/sddm/themes/breeze'

    if not os.path.exists(sddm_conf_dir):
        os.makedirs(sddm_conf_dir)

    if not os.path.exists(sddm_breeze_dir):
        os.makedirs(sddm_breeze_dir)


    copy_from_resources('kde_settings.conf', sddm_conf_dir)
    copy_from_resources('.config/pgd-bg.png', sddm_breeze_dir)
    copy_from_resources('theme.conf.user', sddm_breeze_dir)


def install_plymouth(root: str):
    shared_events.append('Installing Plymouth...')

    if not pacman_install(root, ['plymouth']):
        shared_events.append('Something went wrong while installing Plymouth.')
        return False
    
    copytree_from_resources('michigun', root + '/usr/share/plymouth/themes')
    uncomment_line_in_file(root + '/etc/plymouth/plymouthd.conf', '[Daemon]')
    replace_str_in_file(root + '/etc/plymouth/plymouthd.conf', '#Theme=fade-in', 'Theme=michigun')

    add_mkinitcpio_hook(root, 'plymouth')

    if not mkinitpcio(root):
        shared_events.append('Something went wrong while configuring mkinitcpio.')


def install_gdl_xdg_icon(root: str):
    shared_events.append('Installing GDL XDG icon...')

    target_dir = '/usr/share'

    copy_from_resources('projectgdl-logo.png', root + target_dir)
    result = run_command_in_chroot(root, [
        'xdg-icon-resource', 'install', '--size', '128',
        f'{target_dir}/projectgdl-logo.png'
    ])

    if result.returncode != 0:
        shared_events.append(f'Failed to install an icon: {result.stderr}')
        return False
    
    return True


def install_sayodevice_udev_rule(root: str):
    shared_events.append('Installing SayoDevice udev rule...')

    return copy_from_resources('70-sayo.rules', f'{root}/etc/udev/rules.d')


def copy_sysctl_config(root: str):
    shared_events.append('Copying sysctl config...')

    return copy_from_resources('sysctl.d/99-optimizations.conf', f'{root}/etc/sysctl.d')


def copy_modprobe_config(root: str):
    shared_events.append('Copying modprobe config...')

    return copy_from_resources('gaming.conf', f'{root}/etc/modprobe.d')


def copy_hidden_apps(root: str, username: str):
    shared_events.append('Copying hidden apps...')

    res_dir = get_resources_path()
    user_app_dir = get_user_applications_dir(root, username)

    os.system(f'cp -r {res_dir}/hidden_apps/* {user_app_dir}/')

    fix_user_permissions(root, username)


def copy_fastfetch_config(root: str, username: str):
    shared_events.append('Copying fastfetch config...')

    copy_user_config_dir(root, 'fastfetch', username)
    fix_user_permissions(root, username)


def copy_kde_config(root: str, username: str):
    shared_events.append('Copying KDE config files...')

    user_config_dir = get_user_config_dir(root, username)
    autostart_dir = get_user_autostart_dir(root, username)

    copy_from_resources('.config/autostart/set-gd-wallpaper.desktop', autostart_dir)
    
    copy_from_resources('.config/kdeglobals', user_config_dir)
    copy_from_resources('.config/kwinrulesrc', user_config_dir)
    copy_from_resources('.config/kwinrc', user_config_dir)
    copy_from_resources('.config/kglobalshortcutsrc', user_config_dir)
    copy_from_resources('.config/plasmarc', user_config_dir)
    copy_from_resources('.config/plasma-org.kde.plasma.desktop-appletsrc', user_config_dir)
    copy_from_resources('.config/pgd-bg.png', user_config_dir)
    copy_from_resources('.config/set-gd-wallpaper.sh', user_config_dir)
    copy_from_resources('.config/set-gd-wallpaper.sh', user_config_dir)
    copy_from_resources('.config/gtk-3.0', user_config_dir)
    copy_from_resources('.config/gtk-4.0', user_config_dir)
    copy_from_resources('.config/xsettingsd', user_config_dir)
    
    replace_str_in_file(user_config_dir + '/plasmarc', 'myuser', username)
    replace_str_in_file(user_config_dir + '/set-gd-wallpaper.sh', 'myuser', username)
    replace_str_in_file(autostart_dir + '/set-gd-wallpaper.desktop', 'myuser', username)

    shared_events.append('Adjusting permissions')

    fix_user_permissions(root, username)

    result = run_command_in_chroot(root, [
        'chmod', '7777', f'/home/{username}/.config/set-gd-wallpaper.sh'
    ])
    
    if result.returncode != 0:
        shared_events.append(f'Failed to adjust sgd: {result.stderr}')


def install_geode_installer(root: str):
    shared_events.append('Installing Geode Installer...')
    
    install_latest_gh_package(root, 'GMDProjectL/geode-installer', 'geode-installer')