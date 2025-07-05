from shared import shared_events
from github_utils import *
from gdltypes import InstallInfo
import subprocess

def install_spectacle_fix(installinfo: InstallInfo, root: str) -> bool:
    try:
        shared_events.append("Installing Spectacle Fix")
        release_result = get_latest_github_release("GMDProjectL/spectacle-fix")
        release_binary_url = get_github_rb_url(release_result)
        dest = root + "/usr/bin/spectacle_fix"
        
        download_file(release_binary_url, dest)
        
        process = subprocess.Popen(
            ['chmod', '+x', dest],
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            bufsize=1, universal_newlines=True
        )
        process.wait()

        if process.returncode != 0:
            shared_events.append(f'Failed to give execution permission for {dest} with return code: {process.returncode}')
            return False
        
        with open(f"{root}/home/{installinfo.username}/.config/autostart/spectacle-fix.desktop", "w") as file:
            file.write(f"[Desktop Entry]\nType=Application\nName=Spectacle-Fix\nExec={dest}\nX-GNOME-Autostart-enabled=true")
        
        shared_events.append(f"Installed Spectacle Fix")
    except Exception as e:
        shared_events.append(f'Failed to install Spectacle Fix: {e}')
        return False
    return True