from shared import shared_events
from path_utils import get_user_applications_dir, get_user_hicolor_128_dir
from permission_utils import fix_user_permissions
from resources_utils import copy_from_resources


def copy_gpu_icon(root: str, username: str):
    shared_events.append('Copying GPU icon...')

    icons_dir = get_user_hicolor_128_dir(root, username)
    copy_from_resources('gpu_icon.png', icons_dir)


def copy_lact_desktop_file(root: str, username: str):
    shared_events.append('Copying LACT desktop file...')

    user_app_dir = get_user_applications_dir(root, username)
    copy_from_resources('io.github.ilya_zlobintsev.LACT.desktop', user_app_dir)


def fix_lact_appearance(root: str, username: str):
    shared_events.append('Fixing LACT appearance...')

    copy_gpu_icon(root, username)
    copy_lact_desktop_file(root, username)

    fix_user_permissions(root, username)