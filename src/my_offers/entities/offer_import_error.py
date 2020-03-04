from dataclasses import dataclass
from datetime import datetime


@dataclass
class OfferImportError:
    offer_id: int
    type: str
    message: str
    created_at: datetime
