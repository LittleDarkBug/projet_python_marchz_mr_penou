import bcrypt

class PasswordUtils:
    @staticmethod
    def hash_password(password: str) -> bytes:
        """Convert string password to secure hash"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt)

    @staticmethod
    def verify_password(password: str, hashed: bytes) -> bool:
        """Verify password against stored hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed)