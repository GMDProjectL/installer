from shared import shared_events
from base.resources import copy_from_resources


def install_sayodevice_udev_rule(root: str):
    shared_events.append('Installing SayoDevice udev rule...')

    return copy_from_resources('70-sayo.rules', f'{root}/etc/udev/rules.d')


def copy_sysctl_config(root: str):
    shared_events.append('Copying sysctl config...')

    return copy_from_resources('sysctl.d/99-optimizations.conf', f'{root}/etc/sysctl.d')


def copy_modprobe_config(root: str):
    shared_events.append('Copying modprobe config...')

    return copy_from_resources('gaming.conf', f'{root}/etc/modprobe.d')