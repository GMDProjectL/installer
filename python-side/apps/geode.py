from shared import shared_events
from apps.github import install_latest_gh_package


def install_geode_installer(root: str):
    shared_events.append('Installing Geode Installer...')
    
    install_latest_gh_package(root, 'GMDProjectL/geode-installer', 'geode-installer')