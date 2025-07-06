from shared import shared_events
from base.patching import replace_str_in_file


def patch_distro_release(root: str):
    shared_events.append('Patching distro release...')

    distro_release_path = root + '/usr/lib/os-release'

    replace_str_in_file(distro_release_path, 'Arch Linux', 'Project GDL (Arch Linux)')
    replace_str_in_file(distro_release_path, 'ID=arch', 'ID=projectgdl')
    replace_str_in_file(distro_release_path, 'HOME_URL="https://archlinux.org/"', 'HOME_URL="https://t.me/ProjectGDL"')
    replace_str_in_file(distro_release_path, 'BUG_REPORT_URL="https://bugs.archlinux.org/"', 'BUG_REPORT_URL="https://t.me/ProjectGDL"')
    replace_str_in_file(distro_release_path, 'DOCUMENTATION_URL="https://wiki.archlinux.org/"', 'DOCUMENTATION_URL="https://t.me/ProjectGDL"')
    replace_str_in_file(distro_release_path, 'SUPPORT_URL="https://bbs.archlinux.org/"', 'SUPPORT_URL="https://t.me/ProjectGDL"')
    replace_str_in_file(distro_release_path, 
        'BUG_REPORT_URL="https://gitlab.archlinux.org/groups/archlinux/-/issues"', 
        'BUG_REPORT_URL="https://t.me/ProjectGDL"'
    )
    replace_str_in_file(distro_release_path, 'archlinux-logo', 'projectgdl-logo')