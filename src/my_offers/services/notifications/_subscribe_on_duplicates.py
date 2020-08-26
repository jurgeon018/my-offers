from my_offers.entities import SubscribeOnDuplicatesRequest, SubscribeOnDuplicatesResponse


async def subscribe_on_duplicates(
        request: SubscribeOnDuplicatesRequest,
        realty_user_id: int
) -> SubscribeOnDuplicatesResponse:
    """ Подписать пользователя на обновления дубликатов по всем активным объвлениям. """
    return SubscribeOnDuplicatesResponse(user_already_subscribed=False)
