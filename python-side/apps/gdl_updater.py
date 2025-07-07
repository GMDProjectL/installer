from shared import shared_events
from apps.github import install_latest_gh_package


def install_gdl_updater(root: str):
    shared_events.append('Installing GDL Updater...')
    
    install_latest_gh_package(root, 'GMDProjectL/gdl-updater', 'gdl-updater')