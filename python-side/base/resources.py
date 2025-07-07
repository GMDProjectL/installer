import os
import shutil
from shared import shared_events
from base.path import get_resources_path

def copy_from_resources(file_name: str, target_dir: str) -> bool:
    """
    Copies a file from the resources directory to the target directory.
    """
    res_dir = get_resources_path()
    
    try:
        os.system(f'cp -rf {res_dir}/{file_name} {target_dir}/')
        return True
    except Exception as e:
        shared_events.append(f'Failed to copy {file_name}: {e}')
        return False

def copytree_from_resources(src: str, dst: str) -> bool:
    """
    Copies a directory from the resources directory to the target directory container using copytree.
    """
    res_dir = get_resources_path()
    
    try:
        shutil.copytree(os.path.join(res_dir, src), os.path.join(dst, src), dirs_exist_ok=True)
        return True
    except Exception as e:
        shared_events.append(f'Failed to copy directory {src}: {e}')
        return False

def copy_user_config_dir(root: str, config_dir_name: str, username: str) -> bool:
    res_dir = get_resources_path()
    
    try:
        os.system(f'cp -rf {res_dir}/.config/{config_dir_name} {root}/home/{username}/.config/')
        return True
    except Exception as e:
        shared_events.append(f'Failed to copy config directory {config_dir_name}: {e}')
        return False