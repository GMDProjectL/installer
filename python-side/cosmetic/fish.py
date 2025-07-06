from shared import shared_events
from base.path import get_user_config_dir
from base.resources import copy_from_resources
from base.permissions import fix_user_permissions


def copy_fish_config(root: str, username: str):
    shared_events.append('Copying Fish config files...')

    user_config_dir = get_user_config_dir(root, username)
    copy_from_resources('.config/fish', user_config_dir)

    fix_user_permissions(root, username)