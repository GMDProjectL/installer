from shared import shared_events
from apps.github import *
from base.path import get_user_autostart_dir
from base.resources import copy_from_resources
from base.permissions import fix_user_permissions
from base.process import run_command

def install_spectacle_fix(root: str, username: str) -> bool:
    try:
        shared_events.append("Installing Spectacle Fix")
        release_result = get_latest_github_release("GMDProjectL/spectacle-fix")
        release_binary_url = get_github_rb_url(release_result)
        dest = root + "/usr/bin/spectacle_fix"
        
        download_file(release_binary_url, dest)

        result = run_command(['chmod', '+x', dest])

        if result.returncode != 0:
            shared_events.append(f'Failed to give execution permission for {dest} with return code: {result.returncode}')
            return False
        
        autostart_directory = get_user_autostart_dir(root, username)
        copy_from_resources('.config/autostart/spectacle-fix.desktop', autostart_directory)
        fix_user_permissions(root, username)
        
        shared_events.append(f"Installed Spectacle Fix")
    except Exception as e:
        print(e.with_traceback())
        shared_events.append(f'Failed to install Spectacle Fix: {e}')
        return False
    return True