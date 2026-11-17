from dataclasses import dataclass


@dataclass
class BookAuthor:
    book_author_id: int
    author_id: int
    book_id: int
