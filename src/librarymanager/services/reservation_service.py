from src.librarymanager.models.reservation import Reservation
from src.librarymanager.repositories import (
    book_repository,
    reservation_repository,
    reservation_status_repository,
    user_repository,
)
from src.librarymanager.services import book_service

ACTIVE_STATUS_ID = 1
RETURNED_STATUS_ID = 2
CANCELED_STATUS_ID = 3

READER_ROLE_ID = 1
LIBRARIAN_ROLE_ID = 2


def create_reservation(reader_id: int, book_id: int):
    user = user_repository.get_by_id(reader_id)

    if not user or user.role_id != READER_ROLE_ID:
        raise ValueError("Бронировать может только читатель")

    if not book_repository.get_by_id(book_id):
        raise ValueError("Произведение не найдено")

    if not book_service.is_book_available(book_id):
        raise ValueError("Произведение уже забронировано")

    reservation_repository.create(reader_id, book_id)


def get_all_reservations() -> list[Reservation]:
    return reservation_repository.get_all()


def get_reader_reservations(reader_id: int) -> list[Reservation]:
    return reservation_repository.get_by_reader(reader_id)


def return_book(reservation_id: int, librarian_id: int):
    librarian = user_repository.get_by_id(librarian_id)

    if not librarian or librarian.role_id != LIBRARIAN_ROLE_ID:
        raise ValueError("Принимать возврат может только библиотекарь")

    reservation = reservation_repository.get_by_id(reservation_id)

    if not reservation:
        raise ValueError("Бронирование не найдено")

    if reservation.status_id != ACTIVE_STATUS_ID:
        raise ValueError("Бронирование уже закрыто")

    reservation_repository.mark_returned(reservation_id, librarian_id)


def cancel_reservation(reservation_id: int, reader_id: int):
    reservation = reservation_repository.get_by_id(reservation_id)

    if not reservation:
        raise ValueError("Бронирование не найдено")

    if reservation.reader_id != reader_id:
        raise ValueError("Нельзя отменить чужое бронирование")

    if reservation.status_id != ACTIVE_STATUS_ID:
        raise ValueError("Бронирование уже закрыто")

    reservation_repository.cancel(reservation_id)


def get_status_name(status_id: int) -> str:
    status = reservation_status_repository.get_by_id(status_id)
    return status.name if status else "Unknown"
