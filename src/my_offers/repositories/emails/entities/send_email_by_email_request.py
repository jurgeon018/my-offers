# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client emails`

cian-codegen version: 1.4.1

"""
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class SendEmailByEmailRequest:
    """Модель запроса на отправку письма"""

    address_list: List[str]
    """Список Email-адресов, которым необходимо отправить это письмо"""
    template_name: str
    """Название шаблона письма, который необходимо отправить"""
    parameters: Optional[str] = None
    """Параметры письма в Json в формате строки"""
    transaction_id: Optional[str] = None
    """Идентификатор транзакции"""
