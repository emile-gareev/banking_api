import bcrypt


def hash_password(password: str):
    """Hash password with salt."""
    return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt()).decode('utf8')


def validate_password(password: str, hashed_password: str):
    """Check password hash with database hash."""
    return bcrypt.checkpw(password.encode('utf8'), hashed_password.encode('utf8'))
