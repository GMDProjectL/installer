from shared import shared_events
from base.process import run_command


def generate_fstab(root: str):
    shared_events.append(f'Generating fstab for {root}')

    result = run_command(['genfstab', '-U', root])

    if result.returncode != 0:
        shared_events.append(f'Failed to generate fstab for {root}: {result.stderr}')
        return None

    shared_events.append(f'Generated fstab for {root}: {result.stdout.strip()}')

    return result.stdout.strip()


def clear_mountpoints(root: str):
    shared_events.append(f'Unmounting {root} just in case...')

    result = run_command(['umount', '-Rlf', root])
    if result.returncode != 0:
        shared_events.append(f'{root} not mounted')
        return


def format_fs(partition_name: str, destination: str, bootable = False):
    shared_events.append(f'Formatting {partition_name} partition...')
    partition_device = '/dev/' + partition_name

    result = run_command(['umount', partition_device, destination])
    if result.returncode != 0:
        shared_events.append(f'{destination} not mounted')
    
    format_args = []

    if bootable:
        format_args = ['mkfs.fat', '-F', '32', partition_device]
    else:
        format_args = ['mkfs.ext4', partition_device]

    result = run_command(format_args)
    if result.returncode != 0:
        shared_events.append(f'Failed to format {partition_name} partition: {result.stderr}')
        return False
    
    return True


def nuke_drive(drive_name: str):
    shared_events.append(f'Nuking {drive_name} drive...')

    result = run_command(['wipefs', '-a', '/dev/' + drive_name])
    if result.returncode != 0:
        shared_events.append(f'Failed to wipe {drive_name} drive: {result.stderr}')
        return False
    
    result = run_command(['parted', '/dev/' + drive_name, '--script', 'mklabel', 'gpt'])
    if result.returncode != 0:
        shared_events.append(f'Failed to create GPT label on {drive_name} drive: {result.stderr}')
        return False
    
    result = run_command(['parted', '/dev/' + drive_name, '--script', 'mkpart', 'bootloader', 'fat32', '1MiB', '1024MiB'])
    if result.returncode != 0:
        shared_events.append(f'Failed to make boot partition on {drive_name} drive: {result.stderr}')
        return False
    
    result = run_command(['parted', '/dev/' + drive_name, '--script', 'mkpart', 'ProjectGDL', 'ext4', '1024MiB', '100%'])
    if result.returncode != 0:
        shared_events.append(f'Failed to make main partition on {drive_name} drive: {result.stderr}')
        return False
    
    result = run_command(['mkfs.fat', '-F', '32', '/dev/' + drive_name + '1'])
    if result.returncode != 0:
        shared_events.append(f'Failed to format boot partition on {drive_name} drive: {result.stderr}')
        return False
    
    result = run_command(['mkfs.ext4', '/dev/' + drive_name + '2'])
    if result.returncode != 0:
        shared_events.append(f'Failed to format main partition on {drive_name} drive: {result.stderr}')
        return False
    
    result = run_command(['parted', '/dev/' + drive_name, '--script', 'set', '1', 'boot', 'on'])
    if result.returncode != 0:
        shared_events.append(f'Failed to make boot partition on {drive_name} drive bootable: {result.stderr}')
        return False

    return True
    

def mount_fs(partition_name: str, destination: str):
    partition_device = '/dev/' + partition_name

    result = run_command(['mount', partition_device, destination, '-m'])
    if result.returncode != 0:
        shared_events.append(f'Failed to mount {partition_name} partition: {result.stderr}')
        return False

    shared_events.append(f'Mounted {partition_name} partition to {destination}')

    return True