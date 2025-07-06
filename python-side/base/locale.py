from shared import shared_events
from base.process import run_command_in_chroot
from base.patching import uncomment_line_in_file


def generate_localtime(root: str, region: str, city: str):
    shared_events.append(f'Linking zoneinfo for {root}...')

    result = run_command_in_chroot(root, [
        'ln', '-sf', f'/usr/share/zoneinfo/{region}/{city}', '/etc/localtime'
    ])

    if result.returncode != 0:
        shared_events.append(f'Failed to link zoneinfo for {root}: {result.stderr}')
        return False
    
    return True


def generate_locales(root: str, locales: list):
    shared_events.append(f'Uncommenting locales for {root}...')

    for locale in locales:
        if not locale.endswith('.UTF-8'):
            continue
        uncomment_line_in_file(f'{root}/etc/locale.gen', locale)
    
    result = run_command_in_chroot(root, ['locale-gen'])

    if result.returncode != 0:
        shared_events.append(f'Failed to generate locales for {root}: {result.stderr}')
        return False
    
    return True