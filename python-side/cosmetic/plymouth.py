from shared import shared_events
from base.pacman import pacman_install
from base.resources import copytree_from_resources
from base.patching import uncomment_line_in_file, replace_str_in_file, add_mkinitcpio_hook
from base.admin import mkinitpcio


def install_plymouth(root: str, from_update: bool):
    shared_events.append('Installing Plymouth...')

    if not pacman_install(root, ['plymouth']):
        shared_events.append('Something went wrong while installing Plymouth.')
        return False
    
    copytree_from_resources('michigun', root + '/usr/share/plymouth/themes')

    if not from_update:
        uncomment_line_in_file(root + '/etc/plymouth/plymouthd.conf', '[Daemon]')
        replace_str_in_file(root + '/etc/plymouth/plymouthd.conf', '#Theme=fade-in', 'Theme=michigun')
        add_mkinitcpio_hook(root, 'plymouth')

    if not mkinitpcio(root):
        shared_events.append('Something went wrong while configuring mkinitcpio.')