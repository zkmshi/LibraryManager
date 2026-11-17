from dataclasses import dataclass


@dataclass
class ReservationStatus:
    status_id: int
    name: str
