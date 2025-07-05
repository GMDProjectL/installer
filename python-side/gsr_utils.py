import traceback
from shared import shared_events
from github_utils import install_latest_gh_package
from path_utils import get_user_applications_dir
from patching_utils import replace_str_in_file
from permission_utils import fix_user_permissions
from resources_utils import copy_from_resources, copy_user_config_dir

def install_gsrn(root: str):
    shared_events.append('Installing GSRN...')
    try:
        install_latest_gh_package(root, 'GMDProjectL/gpu-screen-recorder-notification', 'gsrn')
    except Exception as e:
        shared_events.append(f'Failed to install gsrn: {e.with_traceback()}')
        return False
    
    return True

def install_gsrui(root: str):
    shared_events.append('Installing GSR UI...')
    try:
        install_latest_gh_package(root, 'GMDProjectL/gpu-screen-recorder-ui', 'gsrui')
    except Exception as e:
        print(traceback.format_exc())
        shared_events.append(f'Failed to install gsr ui: {traceback.format_exc()}')
        return False
    
    return True

def copy_gsr_handler_stuff(root: str, username: str):
    shared_events.append('Copying GSR config files...')

    user_app_dir = get_user_applications_dir(root, username)

    copy_from_resources('gsr-handler.desktop', user_app_dir)
    copy_from_resources('com.dec05eba.gpu_screen_recorder.png', user_app_dir)

    replace_str_in_file(f'{user_app_dir}/gsr-handler.desktop', 'myuser', username)

    copy_user_config_dir(root, 'gpu-screen-recorder', username)
    copy_from_resources('hidden_apps_kde/com.dec05eba.gpu_screen_recorder.desktop', user_app_dir)

    fix_user_permissions(root, username)
    
    return True
