import os
from shared import shared_events
from base.path import get_user_config_dir, get_user_share_dir, make_user_dirs
from base.resources import copy_from_resources
from base.permissions import fix_user_permissions


def copy_konsole_config(root: str, username: str):
    shared_events.append('Copying Konsole config files...')

    user_config_dir = get_user_config_dir(root, username)
    copy_from_resources('.config/konsolerc', user_config_dir)

    user_share_dir = get_user_share_dir(root, username)
    konsole_proflies_dir = os.path.join(user_share_dir, 'konsole')

    make_user_dirs(root, username, konsole_proflies_dir)

    copy_from_resources('konsole_gdl.profile', konsole_proflies_dir)
    fix_user_permissions(root, username)