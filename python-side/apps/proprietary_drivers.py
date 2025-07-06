from shared import shared_events
import subprocess
from base.pacman import pacman_install
from base.resources import copy_from_resources


def get_lspci():
    '''lspci -k
    '''
    process = subprocess.run(['lspci', '-k'], capture_output=True)
    lspci = process.stdout.decode()

    return lspci


def is_nouveau():
    lspci = get_lspci()
    if 'in use: nouveau' in lspci:
        return True
    
    return False


def is_nvidia():
    lspci = get_lspci()
    if 'in use: nvidia' in lspci:
        return True
    
    return False


def is_broadcom_wl():
    lspci = get_lspci()
    if 'in use: wl' in lspci:
        return True
    
    return False


def try_install_nvidia(root: str):
    if not is_nvidia() and not is_nouveau():
        shared_events.append('Your system doesn\'t have NVIDIA GPU. Skipping.')
        return
    
    shared_events.append('Installing NVIDIA drivers...')
    result = pacman_install(root, 
        [
            'nvidia-dkms', 'nvidia-utils', 
            'nvidia-settings', 'nvidia-prime'
        ]
    )

    if not result:
        shared_events.append('Failed to install NVIDIA drivers')


def try_install_broadcom(root: str):
    if not is_broadcom_wl():
        shared_events.append('Your system doesn\'t have Broadcom WiFi. Skipping.')
        return
    
    shared_events.append('Installing Broadcom drivers...')
    result = pacman_install(root, 
        [
            'linux-headers', 'dkms', 'broadcom-wl-dkms'
        ]
    )

    if not result:
        shared_events.append('Failed to install Broadcom drivers')


def copy_nvidia_prime_steam(root: str):
    shared_events.append('Copying NVIDIA PRIME Steam file...')
    
    return copy_from_resources('steam-prime.desktop', f'{root}/usr/share/applications')