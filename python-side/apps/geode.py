import os
from shared import shared_events
from apps.github import install_latest_gh_package
from base.pacman import pacman_remove


def install_geode_installer(root: str):
    shared_events.append('Installing Geode Installer...')

    if os.path.exists('/geode-installer/main.py'):
        shared_events.append('Removing legacy geode-installer...')
        pacman_remove(root, 'geode-installer')
        return
    
    install_latest_gh_package(root, 'GMDProjectL/geode-linux-installer', 'geode-linux-installer')