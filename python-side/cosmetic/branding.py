from shared import shared_events
from base.resources import copy_from_resources
from base.process import run_command_in_chroot


def install_gdl_xdg_icon(root: str):
    shared_events.append('Installing GDL XDG icon...')

    target_dir = '/usr/share'

    copy_from_resources('projectgdl-logo.png', root + target_dir)
    result = run_command_in_chroot(root, [
        'xdg-icon-resource', 'install', '--size', '128',
        f'{target_dir}/projectgdl-logo.png'
    ])

    if result.returncode != 0:
        shared_events.append(f'Failed to install an icon: {result.stderr}')
        return False
    
    return True