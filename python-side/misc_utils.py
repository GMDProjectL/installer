import os
import requests
from gdltypes import InstallInfo
from shared import shared_events
import shutil
import subprocess
from pacman_utils import pacman_install, pacman_install_from_file
from admin_utils import mkinitpcio


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


def fix_home_permissions(installation_object: InstallInfo, root: str):
    shared_events.append(f'Fixing home permissions for {installation_object.username}...')
    process = subprocess.run([
        'arch-chroot', root,
        'chown', '-R', '1000:1000', '/home/' + installation_object.username
        ], capture_output=True)
    
    if process.returncode != 0:
        shared_events.append(f'Failed to adjust: {process.stderr.decode()}')


def activate_systemd_service(installation_object: InstallInfo, destination: str, service: str, user: str = ''):
    shared_events.append(f'Activating {service}...')

    if user != '':
        try:
            os.system(f'mkdir -p {destination}/home/{user}/.config/systemd/user/default.target.wants')
        except Exception as e:
            print('Ok that exists')
        
        fix_home_permissions(installation_object, destination)

        process = subprocess.run([
            'arch-chroot', destination,
            'ln', '-s', f'/usr/lib/systemd/user/{service}.service', f'/home/{user}/.config/systemd/user/default.target.wants/{service}.service'
            ], capture_output=True)
        
        if process.returncode != 0:
            shared_events.append(f'Failed to activate {service}: {process.stderr.decode()}')
            return False
        
        fix_home_permissions(installation_object, destination)
        
        return True

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
    sddm_breeze_dir = root + '/usr/share/sddm/themes/breeze'

    try:
        os.mkdir(sddm_conf_dir)
    except:
        pass

    shutil.copy(resources_dir + '/kde_settings.conf', sddm_conf_dir + '/kde_settings.conf')


    if not os.path.exists(sddm_breeze_dir):
        shared_events.append('SDDM Breeze theme not found, can\'t patch.')
        return
    
    try:
        shutil.copy(resources_dir + '/.config/pgd-bg.png', sddm_breeze_dir + '/pgdl.png')
        shutil.copy(resources_dir + '/theme.conf.user', sddm_breeze_dir + '/theme.conf.user')
    except Exception as e:
        shared_events.append(f'Failed to apply patch to SDDM Background: {e}')


def install_plymouth(installation_object: InstallInfo, root: str):
    shared_events.append('Installing Plymouth...')

    if not pacman_install(installation_object, root, [
        'plymouth'
    ]):
        shared_events.append('Something went wrong while installing Plymouth.')
        return
    
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        shutil.copytree(script_dir + '/resources/michigun', root + '/usr/share/plymouth/themes/michigun')

        with open(root + '/etc/plymouth/plymouthd.conf') as f:
            content = f.read()
        
        content = content.replace('#[Daemon]', '[Daemon]')
        content = content.replace('#Theme=fade-in', 'Theme=michigun')    

        with open(root + '/etc/plymouth/plymouthd.conf', 'w') as f:
            f.write(content)
    except Exception as e:
        shared_events.append(f'Failed to setup Plymouth theme: {e}')
        return

    with open(root + '/etc/mkinitcpio.conf', 'r') as f:
        lines = f.readlines()
    
    content = ""

    for line in lines:
        if line.startswith('HOOKS') and not 'plymouth' in line:
            content += line.replace(')', ' plymouth)')
        else:
            content += line
    
    with open(root + '/etc/mkinitcpio.conf', 'w') as f:
        f.write(content)

    if not mkinitpcio(installation_object, root):
        shared_events.append('Something went wrong while configuring mkinitcpio.')


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


def install_sayodevice_udev_rule(installation_object: InstallInfo, root: str):
    shared_events.append('Installing SayoDevice udev rule...')
    script_dir = os.path.dirname(os.path.abspath(__file__))
    resources_dir = script_dir + '/resources/'
    target_dir = '/etc/udev/rules.d/'
    rules_name = '70-sayo.rules'

    try:
        shutil.copy(resources_dir + rules_name, root + target_dir + rules_name)
    except Exception as e:
        shared_events.append(f'Failed to copy Sayo udev rule: {e}')


def install_nopasswd_pkrule(installation_object: InstallInfo, root: str):
    shared_events.append('Installing No Polkit Password rule...')
    script_dir = os.path.dirname(os.path.abspath(__file__))
    resources_dir = script_dir + '/resources/'
    target_dir = '/etc/polkit-1/rules.d/'
    rules_name = '40-pknopasswd.rules'

    try:
        shutil.copy(resources_dir + rules_name, root + target_dir + rules_name)
    except Exception as e:
        shared_events.append(f'Failed to copy No Polkit Password rule: {e}')


def copy_sysctl_config(installation_object: InstallInfo, root: str):
    shared_events.append('Copying sysctl config...')
    script_dir = os.path.dirname(os.path.abspath(__file__))
    resources_dir = script_dir + '/resources/'
    target_dir = '/etc/sysctl.d/'
    config_name = '99-optimizations.conf'
    
    try:
        shutil.copy(resources_dir + 'sysctl.d/' + config_name, root + target_dir + config_name)
    except Exception as e:
        shared_events.append(f'Failed to copy sysctl config: {e}')


def copy_modprobe_config(installation_object: InstallInfo, root: str):
    shared_events.append('Copying modprobe config...')
    script_dir = os.path.dirname(os.path.abspath(__file__))
    resources_dir = script_dir + '/resources/'
    target_dir = '/etc/modprobe.d/'
    config_name = 'gaming.conf'
    
    try:
        shutil.copy(resources_dir + 'modprobe.d/' + config_name, root + target_dir + config_name)
    except Exception as e:
        shared_events.append(f'Failed to copy modprobe config: {e}')


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


def copy_nvidia_prime_steam(installation_object: InstallInfo, root: str):
    shared_events.append('Copying NVIDIA PRIME Steam file...')
    script_dir = os.path.dirname(os.path.abspath(__file__))

    res_dir = script_dir + '/resources/'
    app_dir = root + '/usr/share/applications/'

    filename = 'steam-prime.desktop'

    try:
        shutil.copy(res_dir + 'steam-prime.desktop', app_dir + filename)
        os.chown(app_dir + filename, 1000, 1000)
    except Exception as e:
        shared_events.append(f'Failed to copy NVIDIA PRIME Steam file: {e}')


def copy_hidden_apps(installation_object: InstallInfo, root: str):
    shared_events.append('Copying hidden apps...')
    script_dir = os.path.dirname(os.path.abspath(__file__))
    res_dir = script_dir + '/resources/'
    user_app_dir = root + '/home/' + installation_object.username + '/.local/share/applications'

    os.system("mkdir -p " + user_app_dir)
    os.chown(user_app_dir, 1000, 1000)
    os.system("chmod 755 " + user_app_dir)
    os.system(f'cp -r {res_dir}hidden_apps/* {user_app_dir}/')

    process = subprocess.run([
        'arch-chroot', root,
        'chown', '-R', '1000:1000', '/home/' + installation_object.username
        ], capture_output=True)
    
    if process.returncode != 0:
        shared_events.append('Failed to chown hidden apps directory')


def copy_fastfetch_config(installation_object: InstallInfo, root: str):
    shared_events.append('Copying fastfetch config...')
    script_dir = os.path.dirname(os.path.abspath(__file__))
    res_dir = script_dir + '/resources/'
    user_config_dir = root + '/home/' + installation_object.username + '/.config'

    try:
        os.system("mkdir -p " + user_config_dir + '/fastfetch')
    except:
        print('FASTFETCH CONFIG DIRECTORY ALREADY EXISTS?!?!')

    os.system(f'cp -r {res_dir}.config/fastfetch/* {user_config_dir}/fastfetch/')

    fix_home_permissions(installation_object, root)


def copy_kde_config(installation_object: InstallInfo, root: str):
    shared_events.append('Copying KDE config files...')
    script_dir = os.path.dirname(os.path.abspath(__file__))

    dotconfig_dir = script_dir + '/resources/.config'
    user_config_dir = root + '/home/' + installation_object.username + '/.config'
    autostart_dir = user_config_dir + '/autostart'


    try:
        os.mkdir(user_config_dir)
    except:
        shared_events.append('User config directory already exists, copying...')

    try:
        os.mkdir(autostart_dir)
    except:
        shared_events.append('User autostart directory already exists, copying...')


    try:
        shutil.copy(dotconfig_dir + '/kdeglobals', user_config_dir + '/kdeglobals')
    except Exception as e:
        shared_events.append(f'Failed to copy kdeglobals file: {e}')


    try:
        shutil.copy(dotconfig_dir + '/kwinrulesrc', user_config_dir + '/kwinrulesrc')
    except Exception as e:
        shared_events.append(f'Failed to copy kwinrulesrc file: {e}')


    try:
        shutil.copy(dotconfig_dir + '/kglobalshortcutsrc', user_config_dir + '/kglobalshortcutsrc')
    except Exception as e:
        shared_events.append(f'Failed to copy kglobalshortcutsrc file: {e}')


    try:
        shutil.copy(dotconfig_dir + '/plasmarc', user_config_dir + '/plasmarc')
    except Exception as e:
        shared_events.append(f'Failed to copy plasmarc file: {e}')


    try:
        shutil.copy(dotconfig_dir + '/plasma-org.kde.plasma.desktop-appletsrc', user_config_dir + '/plasma-org.kde.plasma.desktop-appletsrc')
    except Exception as e:
        shared_events.append(f'Failed to copy plasma-org.kde.plasma.desktop-appletsrc file: {e}')


    try:
        shutil.copy(dotconfig_dir + '/pgd-bg.png', user_config_dir + '/pgd-bg.png')
    except Exception as e:
        shared_events.append(f'Failed to copy pgd-bg.png file: {e}')


    try:
        shutil.copy(dotconfig_dir + '/set-gd-wallpaper.sh', user_config_dir + '/set-gd-wallpaper.sh')
    except Exception as e:
        shared_events.append(f'Failed to copy set-gd-wallpaper.sh file: {e}')


    try:
        shutil.copy(dotconfig_dir + '/autostart/set-gd-wallpaper.desktop', autostart_dir + '/set-gd-wallpaper.desktop')
    except Exception as e:
        shared_events.append(f'Failed to copy set-gd-wallpaper.desktop file: {e}')

    
    try:
        os.system(f'cp -r "{dotconfig_dir}/gtk-3.0" "{user_config_dir}/"')
        os.system(f'cp -r "{dotconfig_dir}/gtk-4.0" "{user_config_dir}/"')
        os.system(f'cp -r "{dotconfig_dir}/xsettingsd" "{user_config_dir}/"')
    except Exception as e:
        shared_events.append(f'Failed to copy gtk-3.0, gtk-4.0, xsettingsd files: {e}')
    

    with open(user_config_dir + '/plasmarc', 'r') as f:
        plasmarc = f.read()
    
    plasmarc = plasmarc.replace('myuser', installation_object.username)

    with open(user_config_dir + '/plasmarc', 'w') as f:
        f.write(plasmarc)

    try:
        os.mkdir(user_config_dir + '/kdedefaults')
    except Exception as e:
        print("ok that exists")

    with open(user_config_dir + '/kdedefaults/plasmarc', 'w') as f:
        f.write(plasmarc)

    with open(user_config_dir + '/set-gd-wallpaper.sh', 'r') as f:
        sgd = f.read()
    
    sgd = sgd.replace('myuser', installation_object.username)

    with open(user_config_dir + '/set-gd-wallpaper.sh', 'w') as f:
        f.write(sgd)


    with open(autostart_dir + '/set-gd-wallpaper.desktop', 'r') as f:
        sgdd = f.read()
    
    sgdd = sgdd.replace('myuser', installation_object.username)

    with open(autostart_dir + '/set-gd-wallpaper.desktop', 'w') as f:
        f.write(sgdd)


    shared_events.append('Adjusting permissions')

    process = subprocess.run([
        'arch-chroot', root,
        'chown', '-R', '1000:1000', '/home/' + installation_object.username + '/.config'
        ], capture_output=True)
    
    if process.returncode != 0:
        shared_events.append(f'Failed to adjust: {process.stderr.decode()}')


    process = subprocess.run([
        'arch-chroot', root,
        'chmod', '7777', '/home/' + installation_object.username + '/.config/set-gd-wallpaper.sh'
        ], capture_output=True)
    
    if process.returncode != 0:
        shared_events.append(f'Failed to adjust sgd: {process.stderr.decode()}')


def get_latest_gi_release():
    url = 'https://api.github.com/repos/GMDProjectL/geode-installer/releases'
    response = requests.get(url)
    result = response.json()

    return result[0]

def get_gi_zstball():
    release = get_latest_gi_release()
    return release["assets"][0]["browser_download_url"]


def install_geode_installer(installation_object: InstallInfo, root: str):
    shared_events.append('Downloading Geode Installer...')
    zstball_url = get_gi_zstball()

    response = requests.get(zstball_url, stream=True)
    with open(root + '/opt/geode-installer.pkg.tar.zst', 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024): 
            if chunk:
                f.write(chunk)
    
    shared_events.append('Geode Installer downloaded')
    shared_events.append('Installing Geode Installer...')

    pacman_install_from_file(installation_object, root, '/opt/geode-installer.pkg.tar.zst')