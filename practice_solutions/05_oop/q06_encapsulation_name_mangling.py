"""
Topic 05 - Object-Oriented Programming (OOP): Question 6
Problem: Data Encapsulation, Private/Protected Attributes, and Name Mangling.
"""

import hashlib
import uuid


class SecureUserSession:
    """Demonstrates public, protected (_var), and private name-mangled (__var) encapsulation."""

    def __init__(self, username: str, raw_password: str):
        self.username: str = username
        self._session_timeout_seconds: int = 3600
        self.__auth_token: str = uuid.uuid4().hex
        self.__password_hash: str = hashlib.sha256(raw_password.encode()).hexdigest()
        self.__failed_attempts: int = 0

    def verify_password(self, candidate_password: str) -> bool:
        """Verifies candidate password against SHA-256 hash, locking account on 3 failed attempts."""
        candidate_hash = hashlib.sha256(candidate_password.encode()).hexdigest()
        if candidate_hash == self.__password_hash:
            self.__failed_attempts = 0
            return True
        else:
            self.__failed_attempts += 1
            if self.__failed_attempts >= 3:
                raise PermissionError("Account locked due to consecutive failed attempts")
            return False

    def get_masked_token(self) -> str:
        """Returns the token masked showing only the first 4 characters."""
        return f"{self.__auth_token[:4]}****"

    def rotate_token(self, current_password: str) -> str:
        """Rotates session token if the current password matches."""
        if not self.verify_password(current_password):
            raise PermissionError("Invalid password; token rotation aborted")
        self.__auth_token = uuid.uuid4().hex
        return "Successfully Updated"


# Verification & Execution
session = SecureUserSession("dev_admin", "SuperSecret99!")
print(f"User: {session.username}")

auth_success = session.verify_password("SuperSecret99!")
print(f"Authentication with Valid Password: {auth_success}")

token_display = session.get_masked_token()
print(f"Masked Session Token: {token_display}")

rotated = session.rotate_token("SuperSecret99!")
print(f"Rotated Token Generated: {rotated}")

# Direct Private Access Test
print("Direct Private Access (session.__auth_token):")
try:
    _ = session.__auth_token  # type: ignore
except AttributeError as err:
    print(f"Caught: {err}")

# Inspect via Name Mangling
mangled_token = session._SecureUserSession__auth_token
print("Mangled Private Attribute Access (_SecureUserSession__auth_token): Verified Accessible")

# Failed Attempts Lockout Test
print("\nFailed Attempts Lockout Test:")
for attempt in range(1, 4):
    try:
        res = session.verify_password("WrongPassword123")
        print(f"Attempt {attempt} (Bad Pass): {res}")
    except PermissionError as err:
        print(f'Attempt {attempt} (Bad Pass): Caught PermissionError("{err}")')
