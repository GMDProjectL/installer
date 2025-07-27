import os
from shared import shared_events
from apps.github import install_latest_gh_package
from base.process import run_command_in_chroot


def install_zapret(root: str):
    shared_events.append('Installing Zapret...')

    if os.path.exists('/opt/zapret'):
        shared_events.append('Removing legacy zapret...')
        run_command_in_chroot(root, ['rm', '-rf', '/opt/zapret'])
        return
    
    install_latest_gh_package(root, 'GMDProjectL/zapret-installer', 'zapret-installer')