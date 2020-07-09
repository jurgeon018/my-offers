from my_offers.enums import DuplicateTabType, DuplicateType


TAB_TO_TYPES = {
    DuplicateTabType.all: DuplicateType.duplicate,
    DuplicateTabType.duplicate: DuplicateType.duplicate,
    DuplicateTabType.same_building: DuplicateType.same_building,
    DuplicateTabType.similar: DuplicateType.similar,
}


def get_duplicate_type(duplicate_tab: DuplicateTabType) -> DuplicateType:
    return TAB_TO_TYPES.get(duplicate_tab)
