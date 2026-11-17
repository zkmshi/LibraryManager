import hashlib

from src.librarymanager.models.user import User
from src.librarymanager.repositories import user_repository

READER_ROLE_ID = 1
LIBRARIAN_ROLE_ID = 2


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def authenticate(login: str, password: str) -> User | None:
    user = user_repository.get_by_login(login)

    if user is None or user.password_hash != hash_password(password):
        return None

    return user


def _register(first_name, last_name, middle_name, login, password, role_id):
    if not login.strip() or not password:
        raise ValueError("Логин и пароль не могут быть пустыми")

    if user_repository.get_by_login(login):
        raise ValueError("Пользователь с таким логином уже существует")

    user_repository.create(
        first_name=first_name,
        last_name=last_name,
        middle_name=middle_name or None,
        login=login,
        password_hash=hash_password(password),
        role_id=role_id,
    )


def register_reader(first_name, last_name, middle_name, login, password):
    _register(first_name, last_name, middle_name, login, password, READER_ROLE_ID)


def register_librarian(first_name, last_name, middle_name, login, password):
    _register(first_name, last_name, middle_name, login, password, LIBRARIAN_ROLE_ID)
