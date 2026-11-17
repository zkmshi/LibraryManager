from dataclasses import dataclass


@dataclass
class Reservation:
    reservation_id: int
    librarian_id: int | None
    reader_id: int
    book_id: int
    reserved_at: str
    status_id: int
