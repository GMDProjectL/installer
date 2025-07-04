import os
import subprocess
from gdltypes import InstallInfo
from shared import shared_events
import requests
from pacman_utils import pacman_install_from_file


def get_latest_gsrn_release():
    url = 'https://api.github.com/repos/GMDProjectL/gpu-screen-recorder-notification/releases'
    response = requests.get(url)
    result = response.json()

    return result[0]

def get_gsrn_zstd():
    release = get_latest_gsrn_release()
    return release["assets"][0]["browser_download_url"]


def get_latest_gsrui_release():
    url = 'https://api.github.com/repos/GMDProjectL/gpu-screen-recorder-ui/releases'
    response = requests.get(url)
    result = response.json()

    return result[0]

def get_gsrui_zstd():
    release = get_latest_gsrui_release()
    return release["assets"][0]["browser_download_url"]


def download_zstd(url: str, dest: str):
    response = requests.get(url, stream=True)
    with open(dest, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024): 
            if chunk:
                f.write(chunk)

def install_gsrn(installation_object: InstallInfo, root: str):
    try:
        zstd_url = get_gsrn_zstd()
        zstd_dest = '/var/cache/pacman/pkg/gsrn.pkg.tar.zstd'
        download_zstd(zstd_url, root + zstd_dest)
        pacman_install_from_file(installation_object, root, zstd_dest)
        
    except Exception as e:
        shared_events.append(f'Failed to install gsrn: {e}')
        return False
    
    return True

def install_gsrui(installation_object: InstallInfo, root: str):
    try:
        zstd_url = get_gsrui_zstd()
        zstd_dest = '/var/cache/pacman/pkg/gsrui.pkg.tar.zstd'
        download_zstd(zstd_url, root + zstd_dest)
        pacman_install_from_file(installation_object, root, zstd_dest)
        
    except Exception as e:
        shared_events.append(f'Failed to install gsrui: {e}')
        return False
    
    return True

def copy_gsr_handler_stuff(installation_object: InstallInfo, root: str):
    shared_events.append('Copying GSR config files...')
    script_dir = os.path.dirname(os.path.abspath(__file__))

    res_dir = script_dir + '/resources'
    user_app_dir = root + '/home/' + installation_object.username + '/.local/share/applications'
    user_config_dir = root + '/home/' + installation_object.username + '/.config'

    try:
        os.system('mkdir -p ' + user_app_dir)
    except Exception as e:
        print('Maybe it\'s already there?')
    
    try:
        os.system(f'cp {res_dir}/gsr-handler.desktop {user_app_dir}/')
    except Exception as e:
        shared_events.append(f'Failed to copy gsr-handler: {e}')
        return False
    
    try:
        os.system(f'cp {res_dir}/com.dec05eba.gpu_screen_recorder.png {user_app_dir}/')
    except Exception as e:
        shared_events.append(f'Failed to copy gsr-icon: {e}')
        return False
    
    try:
        with open(f'{user_app_dir}/gsr-handler.desktop', 'r') as f:
            gsrdd = f.read()
        
        with open(f'{user_app_dir}/gsr-handler.desktop', 'w') as f:
            f.write(gsrdd.replace('myuser', installation_object.username))

        process = subprocess.run([
            'arch-chroot', root,
            'chown', '-R', '1000:1000', '/home/' + installation_object.username
            ], capture_output=True)
        
        if process.returncode != 0:
            shared_events.append(f'Failed to adjust: {process.stderr.decode()}')
            return False
    except Exception as e:
        shared_events.append(f'Failed to adjust gsr-handler: {e}')
        return False
    
    os.system(f'cp -r "{res_dir}/.config/gpu-screen-recorder" "{user_config_dir}/"')
    os.system(f'cp -r "{res_dir}/hidden_apps_kde/com.dec05eba.gpu_screen_recorder.desktop" "{user_app_dir}/"')
    
    return True
