from shared import shared_events
from path_utils import get_user_config_dir
from resources_utils import copy_from_resources
from permission_utils import fix_user_permissions


def copy_fish_config(root: str, username: str):
    shared_events.append('Copying Fish config files...')

    user_config_dir = get_user_config_dir(root, username)
    copy_from_resources('.config/fish', user_config_dir)

    fix_user_permissions(root, username)