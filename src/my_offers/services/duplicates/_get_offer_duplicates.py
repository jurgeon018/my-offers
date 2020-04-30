from my_offers import entities


async def v1_get_offer_duplicates_public(
        request: entities.GetOfferDuplicatesRequest,
        realty_user_id: int
) -> entities.GetOfferDuplicatesResponse:
    pass
    # todo: https://jira.cian.tech/browse/CD-80224
