from gdltypes import InstallInfo
from shared import shared_events
from github_utils import get_latest_github_release, get_github_rb_url, download_file
from pacman_utils import pacman_install_from_file

def install_hiddify(installation_object: InstallInfo, root: str):
    
    try:
        release_result = get_latest_github_release('GMDProjectL/hiddify')
        zstd_url = get_github_rb_url(release_result)
        zstd_dest = root + '/var/cache/pacman/pkg/hiddify.pkg.tar.zstd'

        download_file(zstd_url, zstd_dest)
        pacman_install_from_file(installation_object, root, zstd_dest)
        
    except Exception as e:
        shared_events.append(f'Failed to install Hiddify: {e}')
        return False
    
    return True