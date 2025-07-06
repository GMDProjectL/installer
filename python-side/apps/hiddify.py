from shared import shared_events
from apps.github import install_latest_gh_package
import traceback

def install_hiddify(root: str):
    shared_events.append('Installing Hiddify...')
    try:
        install_latest_gh_package(root, 'GMDProjectL/hiddify', 'hiddify')
    except Exception as e:
        print(traceback.format_exc())
        shared_events.append(f'Failed to install Hiddify: {e} {traceback.format_exc()}')
        return False
    
    return True

