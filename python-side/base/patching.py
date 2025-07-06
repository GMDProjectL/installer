def replace_str_in_file(file_path: str, old_str: str, new_str: str) -> None:
    with open(file_path, 'r') as file:
        content = file.read()
    
    content = content.replace(old_str, new_str)
    
    with open(file_path, 'w') as file:
        file.write(content)


def uncomment_line_in_file(file_path: str, line_to_uncomment: str) -> None:
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    with open(file_path, 'w') as file:
        for line in lines:
            if line.strip().startswith('#') and line_to_uncomment in line:
                file.write(line.lstrip('#').lstrip())
            else:
                file.write(line)


def add_mkinitcpio_hook(root: str, name: str) -> None:
    with open(root + '/etc/mkinitcpio.conf', 'r') as f:
        lines = f.readlines()
    
    content = ""

    for line in lines:
        if line.startswith('HOOKS') and not name in line:
            content += line.replace(')', f' {name})')
        else:
            content += line
    
    with open(root + '/etc/mkinitcpio.conf', 'w') as f:
        f.write(content)