from datetime import datetime
from typing import Optional

from my_offers.repositories.monolith_cian_announcementapi.entities import PublishTerms


def get_expiration_date(publish_terms: Optional[PublishTerms]) -> Optional[datetime]:
    if publish_terms is not None:
        return publish_terms.expiration_date

    return None


def get_expiration_date_for_mobile(publish_terms: Optional[PublishTerms]) -> Optional[datetime]:
    # не отправляем тонкому клиенту дату истечения срока, если включена автоматическая пролонгация т.к.
    # дата не несёт полезной информации для пользователя, поскольку на деле не является датой окончания публикации,
    # а лишь является датой следующей итерации списания средств
    if publish_terms is None or publish_terms.autoprolong is True:
        return None

    return get_expiration_date(publish_terms=publish_terms)
