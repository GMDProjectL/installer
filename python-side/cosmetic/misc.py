import os
from shared import shared_events
from base.process import run_command_in_chroot
from base.patching import replace_str_in_file
from base.path import get_resources_path, get_user_applications_dir, get_user_autostart_dir, get_user_config_dir
from base.permissions import fix_user_permissions
from base.resources import copy_from_resources, copy_user_config_dir


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
    copy_from_resources('.config/pgd-bg.png', user_config_dir)
    copy_from_resources('.config/set-gd-wallpaper.sh', user_config_dir)
    copy_from_resources('.config/set-gd-wallpaper.sh', user_config_dir)
    copy_from_resources('.config/gtk-3.0', user_config_dir)
    copy_from_resources('.config/gtk-4.0', user_config_dir)
    copy_from_resources('.config/xsettingsd', user_config_dir)
    copy_from_resources('.config/kscreenlockerrc', user_config_dir)

    if not root == '/':
        copy_from_resources('.config/kxkbrc', user_config_dir)
    
    replace_str_in_file(user_config_dir + '/plasmarc', 'myuser', username)
    replace_str_in_file(user_config_dir + '/kscreenlockerrc', 'myuser', username)
    replace_str_in_file(user_config_dir + '/set-gd-wallpaper.sh', 'myuser', username)
    replace_str_in_file(autostart_dir + '/set-gd-wallpaper.desktop', 'myuser', username)

    shared_events.append('Adjusting permissions')

    fix_user_permissions(root, username)

    result = run_command_in_chroot(root, [
        'chmod', '7777', f'/home/{username}/.config/set-gd-wallpaper.sh'
    ])
    
    if result.returncode != 0:
        shared_events.append(f'Failed to adjust sgd: {result.stderr}')