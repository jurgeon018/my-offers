from dataclasses import dataclass


@dataclass
class Coverage:
    searches_count: int
    """Количество поисков"""
    shows_count: int
    """Количество показов"""
    coverage: int
    """Охват в процентах"""
