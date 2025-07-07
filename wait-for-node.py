import subprocess
import time
import sys


def wait_for_server():
    while True:
        try:
            subprocess.check_output(['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', 'http://localhost:4173'])
            break
        except subprocess.CalledProcessError:
            time.sleep(1)

def launch_electron():
    if '--update' in sys.argv:
        subprocess.run(['electron34', 'http://localhost:4173/update'])
    else:
        subprocess.run(['electron34', 'http://localhost:4173'])

def main():
    wait_for_server()
    launch_electron()

if __name__ == "__main__":
    main()