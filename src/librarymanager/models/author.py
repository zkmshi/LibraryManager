from dataclasses import dataclass


@dataclass
class Author:
    author_id: int
    first_name: str
    last_name: str
    middle_name: str | None = None

    @property
    def full_name(self) -> str:
        parts = [self.last_name, self.first_name, self.middle_name]
        return " ".join(p for p in parts if p)
