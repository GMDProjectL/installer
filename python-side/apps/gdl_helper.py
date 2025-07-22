from shared import shared_events
from apps.github import install_latest_gh_package


def install_gdl_helper(root: str):
    shared_events.append('Installing GDL Helper...')
    
    install_latest_gh_package(root, 'GMDProjectL/gdl-helper', 'gdl-helper')