from gdltypes import InstallInfo
from shared import shared_events
import subprocess
from pacman_utils import pacman_install


def get_lspci(installation_object: InstallInfo):
    '''lspci -k
    '''
    process = subprocess.run(['lspci', '-k'], capture_output=True)
    lspci = process.stdout.decode()

    return lspci


def is_nouveau(installation_object: InstallInfo):
    lspci = get_lspci(installation_object)
    if 'in use: nouveau' in lspci:
        return True
    
    return False


def is_nvidia(installation_object: InstallInfo):
    lspci = get_lspci(installation_object)
    if 'in use: nvidia' in lspci:
        return True
    
    return False


def is_broadcom_wl(installation_object: InstallInfo):
    lspci = get_lspci(installation_object)
    if 'in use: wl' in lspci:
        return True
    
    return False


def try_install_nvidia(installation_object: InstallInfo, root: str):
    if not is_nvidia(installation_object) and not is_nouveau(installation_object):
        shared_events.append('Your system doesn\'t have NVIDIA GPU. Skipping.')
        return
    
    shared_events.append('Installing NVIDIA drivers...')
    result = pacman_install(installation_object, root, 
        [
            'nvidia-dkms', 'nvidia-utils', 'nvidia-settings',
            'nvidia-prime'
        ]
    )

    if not result:
        shared_events.append('Failed to install NVIDIA drivers')


def try_install_broadcom(installation_object: InstallInfo, root: str):
    if not is_broadcom_wl(installation_object):
        shared_events.append('Your system doesn\'t have Broadcom WiFi. Skipping.')
        return
    
    shared_events.append('Installing Broadcom drivers...')
    result = pacman_install(installation_object, root, ['linux-headers', 'dkms', 'broadcom-wl-dkms'])

    if not result:
        shared_events.append('Failed to install Broadcom drivers')