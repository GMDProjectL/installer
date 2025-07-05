import os
from shared import shared_events
from path_utils import get_user_config_dir, get_user_share_dir
from resources_utils import copy_from_resources
from permission_utils import fix_user_permissions


def copy_konsole_config(root: str, username: str):
    shared_events.append('Copying Konsole config files...')

    user_config_dir = get_user_config_dir(root, username)
    copy_from_resources('.config/konsolerc', user_config_dir)

    user_share_dir = get_user_share_dir(root, username)
    konsole_proflies_dir = os.path.join(user_share_dir, 'konsole')

    os.makedirs(konsole_proflies_dir)

    copy_from_resources('konsole_gdl.profile', konsole_proflies_dir)
    fix_user_permissions(root, username)