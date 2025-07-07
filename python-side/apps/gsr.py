import os
import traceback
from shared import shared_events
from base.pacman import pacman_remove
from apps.github import install_latest_gh_package
from base.path import get_user_applications_dir, get_user_config_dir
from base.patching import replace_str_in_file
from base.permissions import fix_user_permissions
from base.resources import copy_from_resources, copy_user_config_dir


def try_removing_existing_gsr_packages(root: str):
    pacman_remove(root, ['gpu-screen-recorder-notification-git', 'gpu-screen-recorder-ui-git'])

def install_gsrn(root: str):
    shared_events.append('Installing GSRN...')
    try:
        if root == '/':
            try_removing_existing_gsr_packages(root)
            
        install_latest_gh_package(root, 'GMDProjectL/gpu-screen-recorder-notification', 'gsrn')
    except Exception as e:
        shared_events.append(f'Failed to install gsrn: {e.with_traceback()}')
        return False
    
    return True

def install_gsrui(root: str):
    shared_events.append('Installing GSR UI...')
    try:
        if root == '/':
            try_removing_existing_gsr_packages(root)
        install_latest_gh_package(root, 'GMDProjectL/gpu-screen-recorder-ui', 'gsrui')
    except Exception as e:
        print(traceback.format_exc())
        shared_events.append(f'Failed to install gsr ui: {traceback.format_exc()}')
        return False
    
    return True

def copy_gsr_handler_stuff(root: str, username: str):
    shared_events.append('Copying GSR config files...')

    user_app_dir = get_user_applications_dir(root, username)
    user_config_dir = get_user_config_dir(root, username)
    gsr_ui_config_path = os.path.join(user_config_dir, 'gpu-screen-recorder/config_ui')

    copy_from_resources('gsr-handler.desktop', user_app_dir)
    copy_from_resources('com.dec05eba.gpu_screen_recorder.png', user_app_dir)

    replace_str_in_file(f'{user_app_dir}/gsr-handler.desktop', 'myuser', username)

    if not os.path.exists(gsr_ui_config_path):
        copy_user_config_dir(root, 'gpu-screen-recorder', username)
    else:
        replace_str_in_file(gsr_ui_config_path, 'enable_hotkeys', 'disable_hotkeys')
        
    copy_from_resources('hidden_apps_kde/com.dec05eba.gpu_screen_recorder.desktop', user_app_dir)

    fix_user_permissions(root, username)
    
    return True
