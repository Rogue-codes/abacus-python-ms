import random

import random

def generate_sys_password():
    """Generate a 12-character password efficiently."""
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*"
    return ''.join(random.choices(chars, k=12))