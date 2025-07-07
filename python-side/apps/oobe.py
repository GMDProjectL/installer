import os
import shutil
import requests
import zipfile
from shared import shared_events
from base.path import get_user_autostart_dir
from base.process import run_command_in_chroot
from base.resources import copy_from_resources
from base.permissions import fix_user_permissions


def get_latest_oobe_release():
    url = 'https://api.github.com/repos/GMDProjectL/oobe/releases'
    response = requests.get(url)
    result = response.json()

    return result[0]

def get_zipball():
    release = get_latest_oobe_release()
    return release["zipball_url"]

def copy_directory(src, dst):
    shutil.copytree(src, dst)

def list_directories(path):
    return [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]

def extract_zipball(zipball_url, extract_path):
    response = requests.get(zipball_url, stream=True)
    with open('/tmp/oobe.zip', 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024): 
            if chunk:
                f.write(chunk)
    with zipfile.ZipFile('/tmp/oobe.zip', 'r') as zip_ref:
        zip_ref.extractall(extract_path)

def download_oobe(root: str):
    try:
        zipball_url = get_zipball()
        extract_zipball(zipball_url, '/tmp/oobe')
        directories = list_directories('/tmp/oobe')
        
        if root == '/':
            os.system("rm -rf /opt/oobe")

        copy_directory(os.path.join('/tmp/oobe', directories[0]), root + '/opt/oobe')
        os.remove('/tmp/oobe.zip')
        shutil.rmtree('/tmp/oobe')
    except Exception as e:
        shared_events.append(f'Failed to download OOBE: {e}')
        return False
    
    return True

def clone_oobe(root: str):
    return download_oobe(root)


def adjust_oobe_permissions(root: str):
    shared_events.append('Adjusting OOBE permissions...')

    result = run_command_in_chroot(root, [
        'chmod', '-R', '7777', '/opt/oobe'
    ])
    
    if result.returncode != 0:
        shared_events.append(f'Failed to adjust OOBE permissions: {result.stderr}')
        return False

    result = run_command_in_chroot(root, [
        'chown', '-R', '1000:1000', '/opt/oobe'
    ])
    
    if result.returncode != 0:
        shared_events.append(f'Failed to change OOBE ownership: {result.stderr}')
        return False

    return True


def install_oobe_dependencies(root: str):
    shared_events.append('Installing OOBE dependencies...')

    result = run_command_in_chroot(root, [
        '/opt/oobe/install_dependencies.sh'
    ])
    
    if result.returncode != 0:
        shared_events.append(f'Failed to install OOBE dependencies: {result.stderr}')
        return False
    
    return True


def create_oobe_autostart(root: str, username: str):
    shared_events.append(f'Installing OOBE autostart...')

    autostart_directory = get_user_autostart_dir(root, username)

    copy_from_resources('.config/autostart/oobe.desktop', autostart_directory)
    fix_user_permissions(root, username)
    
    return True