# pylint: skip-file
"""

Code generated by new-codegen; DO NOT EDIT.

To re-generate, run `new-codegen generate-client my-offers`

new-codegen version: 4.0.2

"""
from cian_automation.context import LazyImport
from .clients.public_v1_actions_archive_offer import PublicV1ActionsArchiveOffer
from .clients.public_v1_actions_delete_offer import PublicV1ActionsDeleteOffer
from .clients.public_v1_actions_update_edit_date import PublicV1ActionsUpdateEditDate
from .clients.public_v1_get_offers import PublicV1GetOffers
from .clients.public_v2_get_offers import PublicV2GetOffers


class MyOffers(metaclass=LazyImport):
    public_v1_actions_archive_offer: PublicV1ActionsArchiveOffer
    public_v1_actions_delete_offer: PublicV1ActionsDeleteOffer
    public_v1_actions_update_edit_date: PublicV1ActionsUpdateEditDate
    public_v1_get_offers: PublicV1GetOffers
    public_v2_get_offers: PublicV2GetOffers
