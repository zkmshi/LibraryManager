from dataclasses import dataclass


@dataclass
class Book:
    book_id: int
    title: str
    isbn: str
