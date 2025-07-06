import requests
from typing import Any
from base.pacman import pacman_install_from_file

def get_latest_github_release(url: str) -> Any:
    response = requests.get(f"https://api.github.com/repos/{url}/releases")
    result = response.json()

    print(result)

    return result[0]

def get_github_rb_url(release_result: Any) -> str:
    return release_result["assets"][0]["browser_download_url"]

def download_file(url: str, dest: str) -> None:
    response = requests.get(url, stream=True)
    with open(dest, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024): 
            if chunk:
                f.write(chunk)

def download_latest_zstd_package(url: str, dest: str) -> None:
    release = get_latest_github_release(url)
    zstd_url = get_github_rb_url(release)
    download_file(zstd_url, dest)

def install_latest_gh_package(root: str, url: str, name: str) -> None:
    zstd_rel_dest = f'/var/cache/pacman/pkg/{name}.pkg.tar.zstd'
    download_latest_zstd_package(url, root + zstd_rel_dest)
    pacman_install_from_file(root, zstd_rel_dest)