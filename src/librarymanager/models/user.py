from dataclasses import dataclass


@dataclass
class User:
    user_id: int
    first_name: str
    last_name: str
    middle_name: str | None
    login: str
    password_hash: str
    role_id: int
