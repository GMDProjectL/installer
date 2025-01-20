import os
import shutil
from gdltypes import InstallInfo
from shared import shared_events
import subprocess
import requests
import zipfile


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
        copy_directory(os.path.join('/tmp/oobe', directories[0]), root + '/opt/oobe')
        os.remove('/tmp/oobe.zip')
        shutil.rmtree('/tmp/oobe')
    except Exception as e:
        shared_events.append(f'Failed to download OOBE: {e}')
        return False
    
    return True

def clone_oobe(installation_object: InstallInfo, root: str):
    return download_oobe(root)


def adjust_permissions(installation_object: InstallInfo, root: str):
    process = subprocess.Popen([
        'arch-chroot', root,
        'chmod', '-R', '7777', '/opt/oobe'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, universal_newlines=True)
    
    for line in iter(process.stdout.readline, ''):
        shared_events.append(f'Changing permissions: {line.strip()}')
    process.wait()
    
    if process.returncode != 0:
        for line in iter(process.stderr.readline, ''):
            shared_events.append(f'Failed to change OOBE permissions: {line.strip()}')
        
        return False


    process = subprocess.Popen([
        'arch-chroot', root,
        'chown', '-R', installation_object.username, '/opt/oobe'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, universal_newlines=True)
    
    for line in iter(process.stdout.readline, ''):
        shared_events.append(f'Changing ownership: {line.strip()}')
    process.wait()
    
    if process.returncode != 0:
        for line in iter(process.stderr.readline, ''):
            shared_events.append(f'Failed to change OOBE ownership: {line.strip()}')
        
        return False
    
    return True


def install_oobe_dependencies(installation_object: InstallInfo, root: str):
    process = subprocess.Popen([
        'arch-chroot', root,
        '/opt/oobe/install_dependencies.sh'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, universal_newlines=True)
    
    for line in iter(process.stdout.readline, ''):
        shared_events.append(f'Installing OOBE dependencies: {line.strip()}')
    process.wait()
    
    if process.returncode != 0:
        for line in iter(process.stderr.readline, ''):
            shared_events.append(f'Failed to install: {line.strip()}')
        
        return False
    
    return True


def create_oobe_autostart(installation_object: InstallInfo, root: str):
    username = installation_object.username
    autostart_directory = '/home/' + username + '/.config/autostart'
    script_dir = os.path.dirname(os.path.abspath(__file__))

    shared_events.append(f'Installing OOBE autostart...')

    try:
        shutil.copy(script_dir + '/resources/.config/autostart/oobe.desktop', root + autostart_directory + '/oobe.desktop')
    except Exception as e:
        shared_events.append(f'Failed to install OOBE autostart: {str(e)}')
        return
    
    process = subprocess.Popen([
        'arch-chroot', root,
        'chown', username, autostart_directory + '/oobe.desktop'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, universal_newlines=True)
    
    for line in iter(process.stdout.readline, ''):
        shared_events.append(f'Installing OOBE autostart perms: {line.strip()}')
    process.wait()
    
    if process.returncode != 0:
        for line in iter(process.stderr.readline, ''):
            shared_events.append(f'Failed to install OOBE autostart perms: {line.strip()}')
        
        return False
    
    return True