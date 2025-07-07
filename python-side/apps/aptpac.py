from shared import shared_events
from apps.github import install_latest_gh_package
from base.pacman import blacklist_package


def install_aptpac(root: str):
    shared_events.append('Installing aptpac...')

    blacklist_package(root, 'aptpac')
    
    install_latest_gh_package(root, 'GMDProjectL/aptpac', 'aptpac')