import subprocess
import time
import sys
import os

# chdir to the current script dir
os.chdir(os.path.dirname(os.path.abspath(__file__)))

doesDev = False

def wait_for_server():
    global doesDev
    while True:
        try:
            subprocess.check_output(['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', 'http://localhost:669'])
            subprocess.check_output(['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', 'http://localhost:5173' if doesDev else 'http://localhost:4173'])
            break
        except subprocess.CalledProcessError:
            time.sleep(1)

def launch_electron():
    global doesDev

    electron_command = ['electron34', "./electron-init.js", '--icon', './python-side/resources/projectgdl-logo.png', '--url']

    if '--update' in sys.argv:
        subprocess.run(electron_command + ['http://localhost:5173/update' if doesDev else 'http://localhost:4173/update'])
    else:
        subprocess.run(electron_command + ['http://localhost:5173' if doesDev else 'http://localhost:4173'])

def main():
    global doesDev
    if '--dev' in sys.argv:
        doesDev = True

    wait_for_server()
    launch_electron()

if __name__ == "__main__":
    main()