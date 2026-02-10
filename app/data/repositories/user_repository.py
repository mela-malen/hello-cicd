"""User model and repository for admin authentication."""

from dataclasses import dataclass, field
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash


@dataclass
class User:
    """Admin user with secure password storage.

    Passwords are hashed using Werkzeug's PBKDF2 implementation.
    Never stores plain text passwords.
    """

    username: str
    password_hash: str = ""
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, password: str) -> None:
        """Hash and store a password.

        Args:
            password: Plain text password to hash
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verify a password against the stored hash.

        Args:
            password: Plain text password to verify

        Returns:
            True if password matches, False otherwise
        """
        return check_password_hash(self.password_hash, password)


class UserRepository:
    """In-memory storage for User entities."""

    def __init__(self):
        self._users: dict[str, User] = {}

    def save(self, user: User) -> User:
        """Save a user to the repository."""
        self._users[user.username] = user
        return user

    def find_by_username(self, username: str) -> User | None:
        """Find a user by username."""
        return self._users.get(username)

    def exists(self, username: str) -> bool:
        """Check if a user exists."""
        return username in self._users

    def get_all(self) -> list[User]:
        """Get all users."""
        return list(self._users.values())
