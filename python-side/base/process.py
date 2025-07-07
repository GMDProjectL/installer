import subprocess
from shared import shared_events
from gdltypes import CommandOutput

def run_command(command: list) -> CommandOutput:
    """
    Run a shell command with real-time output capture.
    """

    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )
    
    stdout_lines = []
    stderr_lines = []
    
    # Читаем stdout в реальном времени
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            line = output.strip()
            stdout_lines.append(line)
            if command[0] == 'arch-chroot':
                shared_events.append(f'Running {command[2]} in chroot: {line}')
            else:
                shared_events.append(f'Running {command[0]}: {line}')
    
    # Читаем stderr
    stderr_output = process.stderr.read()
    if stderr_output:
        stderr_lines = stderr_output.strip().split('\n')
    
    shared_events.append(f'Return code of {command[0]}: {process.returncode}')

    return CommandOutput(
        stdout='\n'.join(stdout_lines),
        stderr='\n'.join(stderr_lines),
        returncode=process.returncode
    )

def run_command_in_chroot(root: str, command: list) -> CommandOutput:
    """
    Run a shell command in the chroot environment and return the exit code, stdout, and stderr.
    """
    full_command = ['arch-chroot', root] + command

    if root == '/':
        return run_command(command)

    return run_command(full_command)