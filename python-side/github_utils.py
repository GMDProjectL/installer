import requests
from typing import Any

def get_latest_github_release(url: str) -> Any:
    response = requests.get(f"https://api.github.com/repos/${url}/release")
    result = response.json()

    return result[0]

def get_github_rb_url(release_result: Any) -> str:
    return release_result["assets"][0]["browser_download_url"]

def download_file(url: str, dest: str) -> None:
    response = requests.get(url, stream=True)
    with open(dest, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024): 
            if chunk:
                f.write(chunk)