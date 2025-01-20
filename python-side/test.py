import requests
import zipfile
import shutil
import os


def get_latest_oobe_release():
    url = 'https://api.github.com/repos/GMDProjectL/oobe/releases'
    response = requests.get(url)
    result = response.json()

    return result[0]

def get_zipball():
    release = get_latest_oobe_release()
    return release["zipball_url"]

def copy_directory(src, dst):
    shutil.copytree(src, dst)

def list_directories(path):
    return [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]

def extract_zipball(zipball_url, extract_path):
    response = requests.get(zipball_url, stream=True)
    with open('oobe.zip', 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024): 
            if chunk:
                f.write(chunk)
    with zipfile.ZipFile('oobe.zip', 'r') as zip_ref:
        zip_ref.extractall(extract_path)

def download_oobe():
    zipball_url = get_zipball()
    extract_zipball(zipball_url, '/tmp/oobe')
    directories = list_directories('/tmp/oobe')
    copy_directory(os.path.join('/tmp/oobe', directories[0]), '/opt/oobe')
    os.remove('oobe.zip')
    shutil.rmtree('/tmp/oobe')

def main():
    download_oobe()

if __name__ == "__main__":
    main()