import os
from permission_utils import fix_user_permissions

def get_resources_path() -> str:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, 'resources')

def get_resources_config_dir() -> str:
    return os.path.join(get_resources_path(), '.config')

def make_user_dirs(root: str, username: str, path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)
        fix_user_permissions(root, username)

def get_user_home_dir(root: str, username: str) -> str:
    path = os.path.join(root, 'home', username)
    make_user_dirs(root, username, path)
    return path

def get_user_applications_dir(root: str, username: str) -> str:
    path = os.path.join(get_user_home_dir(root, username), '.local', 'share', 'applications')
    make_user_dirs(root, username, path)
    return path

def get_user_config_dir(root: str, username: str) -> str:
    path = os.path.join(get_user_home_dir(root, username), '.config')
    make_user_dirs(root, username, path)
    return path

def get_user_share_dir(root: str, username: str) -> str:
    path = os.path.join(get_user_home_dir(root, username), '.local/share')
    make_user_dirs(root, username, path)
    return path

def get_user_hicolor_128_dir(root: str, username: str) -> str:
    path = os.path.join(get_user_share_dir(root, username), 'icons/hicolor/128x128/apps')
    make_user_dirs(root, username, path)
    return path

def get_user_autostart_dir(root: str, username: str) -> str:
    path = os.path.join(get_user_config_dir(root, username), 'autostart')
    make_user_dirs(root, username, path)
    return path

def get_user_kdedefaults_dir(root: str, username: str) -> str:
    path = os.path.join(get_user_config_dir(root, username), 'kdedefaults')
    make_user_dirs(root, username, path)
    return path