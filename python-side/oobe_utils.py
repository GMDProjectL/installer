import os
import shutil
from gdltypes import InstallInfo
from shared import shared_events
import subprocess


def clone_oobe(installation_object: InstallInfo, root: str):
    url = 'https://github.com/GMDProjectL/oobe'
    process = subprocess.Popen([
        'arch-chroot', root,
        'git', 'clone', 
        url, '/opt/oobe'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, universal_newlines=True)
    
    for line in iter(process.stdout.readline, ''):
        shared_events.append(f'Cloning OOBE: {line.strip()}')
    process.wait()
    
    if process.returncode != 0:
        for line in iter(process.stderr.readline, ''):
            shared_events.append(f'Failed to clone OOBE: {line.strip()}')
        
        return False
    
    return True


def adjust_permissions(installation_object: InstallInfo, root: str):
    process = subprocess.Popen([
        'arch-chroot', root,
        'chmod', '-R', '7777', '/opt/oobe/'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, universal_newlines=True)
    
    for line in iter(process.stdout.readline, ''):
        shared_events.append(f'Changing permissions: {line.strip()}')
    process.wait()
    
    if process.returncode != 0:
        for line in iter(process.stderr.readline, ''):
            shared_events.append(f'Failed to change OOBE permissions: {line.strip()}')
        
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
        return True
    except Exception as e:
        shared_events.append(f'Failed to install OOBE autostart: {str(e)}')