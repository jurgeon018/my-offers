from attr import dataclass


@dataclass
class QaGetByIdRequest:
    offer_id: int
    user_id: int
