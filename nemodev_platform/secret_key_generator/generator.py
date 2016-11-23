import os

from django.utils.crypto import get_random_string

chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'

SECRET_KEY_FILE_NAME = 'nemodev_platform/configs/secret_key.txt'


# Получить SECRET_KEY приложения
def get_app_secret_key(base_dir):
    file_path = os.path.join(base_dir, SECRET_KEY_FILE_NAME)
    if os.path.exists(file_path):
        with open(file_path) as f:
            secret_key = f.read().strip()
    else:
        secret_key = get_random_string(50, chars)
        with open(file_path, 'w') as f:
            f.write(secret_key)
    return secret_key




