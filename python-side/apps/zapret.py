import os
from shared import shared_events
from apps.github import install_latest_gh_package


def install_zapret(root: str):
    shared_events.append('Installing Zapret...')
    
    install_latest_gh_package(root, 'GMDProjectL/zapret-installer', 'zapret-installer')