import os
from shared import shared_events
from pacman_utils import pacman_install
from process_utils import run_command_in_chroot
from patching_utils import replace_str_in_file
from resources_utils import copy_from_resources


def update_grub(root: str):
    shared_events.append('Generating GRUB config...')

    result = run_command_in_chroot(root, ['grub-mkconfig', '-o', '/boot/grub/grub.cfg'])
    
    if result.returncode != 0:
        shared_events.append(f'Failed to generate GRUB config: {result.stderr}')
        return False
    
    shared_events.append('Installed GRUB successfully!')
    return True


def install_grub(root: str):
    shared_events.append('Installing GRUB...')

    result = run_command_in_chroot(root, [
        'grub-install', '--target=x86_64-efi',
        '--efi-directory=/boot/efi', '--bootloader-id=ProjectGDL'
    ])
    
    if result.returncode != 0:
        shared_events.append(f'Failed to install GRUB: {result.stderr}')
        return False

    update_grub(root)
    
    return True


def patch_default_grub(root: str):
    shared_events.append('Patching default grub...')

    pacman_install(root, ['os-prober', 'grub-theme-vimix'])

    if not os.path.exists(root + '/usr/share/gdlbg'):
        os.makedirs(root + '/usr/share/gdlbg')
    
    copy_from_resources('.config/pgd-bg.png', root + '/usr/share/gdlbg')

    replace_str_in_file(root + '/etc/default/grub', 'GRUB_DISTRIBUTOR="Arch"', 'GRUB_DISTRIBUTOR="ProjectGDL"')
    replace_str_in_file(root + '/etc/default/grub', 'loglevel=3 quiet', 'loglevel=3 quiet splash radeon.dpm=0 nmi_watchdog=0 mitigations=off tsc=reliable clocksource=tsc no_debug_objects dma_debug=off highres=on no_timer_check no-kvmclock nomca nomce nosoftlockup nowatchdog powersave=off selinux=0 apparmor=0')
    replace_str_in_file(root + '/etc/default/grub', '#GRUB_BACKGROUND="/path/to/wallpaper"', 'GRUB_BACKGROUND="/usr/share/gdlbg/pgd-bg.png"')
    replace_str_in_file(root + '/etc/default/grub', '#GRUB_DISABLE_OS_PROBER=false', 'GRUB_DISABLE_OS_PROBER=false')
    replace_str_in_file(root + '/etc/default/grub', 'GRUB_GFXMODE=auto', 'GRUB_GFXMODE=1920x1080')
