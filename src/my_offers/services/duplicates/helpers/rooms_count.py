from typing import Optional, Tuple


def get_possible_room_counts(rooms_count: Optional[int]) -> Optional[Tuple[str, str, str]]:
    if not rooms_count:
        return None
    return str(rooms_count - 1), str(rooms_count), str(rooms_count + 1)
