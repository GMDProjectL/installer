import os

def fix_user_permissions(root: str, username: str) -> None:
    user_home = os.path.join(root, 'home', username)
    
    os.system(f'chown -R 1000:1000 {user_home}')