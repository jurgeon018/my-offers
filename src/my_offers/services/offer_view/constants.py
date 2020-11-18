from my_offers.repositories.monolith_cian_announcementapi.entities.bargain_terms import Currency


SQUARE_METER_SYMBOL = 'м²'

CURRENCY = {
    Currency.rur: '₽',
    Currency.usd: '$',
    Currency.eur: '€',
}

RELEVANCE_DUE_DATE_FORMAT = '%d %B %Y года'

RELEVANCE_DUE_DATE_MESSAGE_TEXT = (
    'Допустимый срок публикации истекает {formatted_date}, затем объявление будет автоматически снято с публикации. '
    'Если объявление актуально, подтвердите это. Если неактуально, вы можете перенести его в архив.'
)

RELEVANCE_REGULAR_MESSAGE_TEXT = (
    'Если объявление актуально, подтвердите это. Если неактуально, вы можете перенести его в архив.'
)
