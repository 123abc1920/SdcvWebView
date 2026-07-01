from dataclasses import dataclass


@dataclass
class UserDTO:
    """Data Transfer Object (DTO) for user information."""

    user_name: str
    """Unique name (login) of the user in the system."""
