from gdltypes import InstallInfo
from shared import shared_events
import requests
from pacman_utils import pacman_install_from_file


def get_latest_hiddify_release():
    url = 'https://api.github.com/repos/GMDProjectL/hiddify/releases'
    response = requests.get(url)
    result = response.json()

    return result[0]

def get_zstd():
    release = get_latest_hiddify_release()
    return release["assets"][0]["browser_download_url"]

def download_zstd(url: str, dest: str):
    response = requests.get(url, stream=True)
    with open(dest, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024): 
            if chunk:
                f.write(chunk)

def install_hiddify(installation_object: InstallInfo, root: str):
    try:
        zstd_url = get_zstd()
        zstd_dest = '/var/cache/pacman/pkg/hiddify.pkg.tar.zstd'
        download_zstd(zstd_url, root + zstd_dest)
        pacman_install_from_file(installation_object, root, zstd_dest)
        
    except Exception as e:
        shared_events.append(f'Failed to install Hiddify: {e}')
        return False
    
    return True