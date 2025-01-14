import os
from gdltypes import InstallInfo
from shared import shared_events
import shutil
import subprocess


def generate_fstab(installation_object: InstallInfo, destination: str):
    shared_events.append(f'Generating fstab for {destination}')

    process = subprocess.run(['genfstab', '-U', destination], capture_output=True)
    fstab = process.stdout.decode()

    shared_events.append(f'Generated fstab for {destination}: {fstab}')

    return fstab


def generate_localtime(installation_object: InstallInfo, root: str):
    shared_events.append(f'Linking zoneinfo for {root}...')

    process = subprocess.run([
        'arch-chroot', root, 
        'ln', '-sf', ('/usr/share/zoneinfo/' 
        + f'{installation_object.timezoneRegion}/{installation_object.timezoneInfo}'), 
        '/etc/localtime'
    ], capture_output=True)

    if process.returncode != 0:
        shared_events.append(f'Failed to link zoneinfo for {root}: {process.stderr.decode()}')
        return False
    
    return True


def generate_locales(installation_object: InstallInfo, root: str, locales: list):
    shared_events.append(f'Uncommenting locales for {root}...')

    with open(f'{root}/etc/locale.gen', 'r') as file:
        lines = file.readlines()

    with open(f'{root}/etc/locale.gen', 'w') as file:
        for line in lines:
            if any(locale in line for locale in locales):
                file.write(line.replace('#', '', 1))
            else:
                file.write(line)
            file.write('\n')

    process = subprocess.run([
        'arch-chroot', root, 
        'locale-gen'
    ], capture_output=True)

    if process.returncode != 0:
        shared_events.append(f'Failed to generate locales for {root}: {process.stderr.decode()}')
        return False
    
    return True


def activate_systemd_service(installation_object: InstallInfo, destination: str, service: str):
    shared_events.append(f'Activating {service}...')

    process = subprocess.run([
        'arch-chroot', destination,
        'systemctl', 'enable', service
        ], capture_output=True)
    
    if process.returncode != 0:
        shared_events.append(f'Failed to activate {service}: {process.stderr.decode()}')
        return False
    
    return True


def patch_distro_release(installation_object: InstallInfo, root: str):
    shared_events.append('Patching distro release...')
    # changing /usr/lib/os-release
    with open(root + '/usr/lib/os-release', 'r') as f:
        content = f.read()
        content = content.replace("Arch Linux", "Project GDL (Arch Linux)")
        content = content.replace("ID=arch", "ID=projectgdl")
        content = content.replace('HOME_URL="https://archlinux.org/"', 'HOME_URL="https://t.me/ProjectGDL"')
        content = content.replace('BUG_REPORT_URL="https://bugs.archlinux.org/"', 'BUG_REPORT_URL="https://t.me/ProjectGDL"')
        content = content.replace('DOCUMENTATION_URL="https://wiki.archlinux.org/"', 'DOCUMENTATION_URL="https://t.me/ProjectGDL"')
        content = content.replace('SUPPORT_URL="https://bbs.archlinux.org/"', 'SUPPORT_URL="https://t.me/ProjectGDL"')
        content = content.replace(
            'BUG_REPORT_URL="https://gitlab.archlinux.org/groups/archlinux/-/issues"', 
            'BUG_REPORT_URL="https://t.me/ProjectGDL"'
        )
        content = content.replace(
            'archlinux-logo', 
            'projectgdl-logo'
        )
    
    with open(root + '/usr/lib/os-release', 'w') as f:
        f.write(content)


def patch_sddm_theme(installation_object: InstallInfo, root: str):
    shared_events.append('Patching default SDDM theme...')
    script_dir = os.path.dirname(os.path.abspath(__file__))
    resources_dir = script_dir + '/resources'
    sddm_conf_dir = root + '/etc/sddm.conf.d'

    try:
        os.mkdir(sddm_conf_dir)
    except:
        pass

    shutil.copy(resources_dir + '/kde_settings.conf', sddm_conf_dir + '/kde_settings.conf')


def install_gdl_xdg_icon(installation_object: InstallInfo, root: str):
    shared_events.append('Installing GDL XDG icon...')
    script_dir = os.path.dirname(os.path.abspath(__file__))
    resources_dir = script_dir + '/resources'
    target_dir = '/usr/share'

    shutil.copy(resources_dir + '/projectgdl-logo.png', root + target_dir + '/projectgdl-logo.png')

    result = os.system(f'arch-chroot {root} xdg-icon-resource install --size 128 "{target_dir + '/projectgdl-logo.png'}"')

    if result != 0:
        shared_events.append('Failed to install an icon')
        return False
    
    return True


def put_essentials_on_desktop(installation_object: InstallInfo, root: str):
    shared_events.append('Placing essentials on desktop...')

    if not os.path.exists(root + '/home/' + installation_object.username + '/Desktop'):
        try:
            os.makedirs(root + '/home/' + installation_object.username + '/Desktop')
            os.chown(pamac_desktop_file, 1000, 1000)
        except:
            shared_events.append('Failed to create and chown a desktop directory')
            return False

    pamac_desktop_file_orig = root + '/usr/share/applications/org.manjaro.pamac.manager.desktop'
    pamac_desktop_file = root + '/home/' + installation_object.username + '/Desktop/pamac-manager.desktop'

    try:
        shutil.copy(pamac_desktop_file_orig, pamac_desktop_file)
        os.chown(pamac_desktop_file, 1000, 1000)
    except:
        shared_events.append('Failed to copy and chown a desktop file')