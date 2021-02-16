from my_offers import entities


async def v1_get_offers_counters_mobile_public(
        request: entities.GetOffersCountersMobileRequest,
        realty_user_id: int,
) -> entities.GetOffersCountersMobileResponse:
    # TODO: Реализовать обработку входных данных CD-100659
    # search_text: str = prepare_search_text(request.search)

    # TODO: Реализовать логику-репозиторий получения данных счетчика CD-100660
    # result = await get_mobile_counters(data)

    return entities.GetOffersCountersMobileResponse(
        rent=entities.GetOffersCountersMobileCounter(
            total=3998,
            flat=233,
            suburban=3423,
            commercial=342,
        ),
        sale=entities.GetOffersCountersMobileCounter(
            total=4001,
            flat=234,
            suburban=3424,
            commercial=343,
        ),
        archieved=entities.GetOffersCountersMobileArchivedInactiveCounter(
            total=3654,
            rent=232,
            sale=3422,
        ),
        inactive=entities.GetOffersCountersMobileArchivedInactiveCounter(
            total=3,
            rent=1,
            sale=2,
        ),
    )
