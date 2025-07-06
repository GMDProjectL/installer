import os
from shared import shared_events
from base.resources import copy_from_resources


def patch_sddm_theme(root: str):
    shared_events.append('Patching default SDDM theme...')

    sddm_conf_dir = root + '/etc/sddm.conf.d'
    sddm_breeze_dir = root + '/usr/share/sddm/themes/breeze'

    if not os.path.exists(sddm_conf_dir):
        os.makedirs(sddm_conf_dir)

    if not os.path.exists(sddm_breeze_dir):
        os.makedirs(sddm_breeze_dir)


    copy_from_resources('kde_settings.conf', sddm_conf_dir)
    copy_from_resources('.config/pgd-bg.png', sddm_breeze_dir)
    copy_from_resources('theme.conf.user', sddm_breeze_dir)