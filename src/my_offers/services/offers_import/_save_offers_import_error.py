from typing import List

from my_offers import entities
from my_offers.repositories.postgresql.offer_import_error import upsert_offer_import_errors


async def save_offers_import_error(errors: List[entities.OfferImportError]) -> None:
    chunk_size = 100
    for i in range(0, len(errors), chunk_size):
        await upsert_offer_import_errors(errors[i: i + chunk_size])
