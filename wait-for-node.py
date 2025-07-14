import subprocess
import time
import sys

doesDev = False

def wait_for_server():
    global doesDev
    while True:
        try:
            subprocess.check_output(['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', 'http://localhost:5173' if doesDev else 'http://localhost:4173'])
            break
        except subprocess.CalledProcessError:
            time.sleep(1)

def launch_electron():
    global doesDev
    if '--update' in sys.argv:
        subprocess.run(['electron34', "./electron-init.js", '--icon', './python-side/resources/projectgdl-logo.png', '--url', 'http://localhost:5173/update' if doesDev else 'http://localhost:4173/update'])
    else:
        subprocess.run(['electron34', "./electron-init.js", '--icon', './python-side/resources/projectgdl-logo.png', '--url', 'http://localhost:5173' if doesDev else ''])

def main():
    global doesDev
    if '--dev' in sys.argv:
        doesDev = True

    wait_for_server()
    launch_electron()

if __name__ == "__main__":
    main()