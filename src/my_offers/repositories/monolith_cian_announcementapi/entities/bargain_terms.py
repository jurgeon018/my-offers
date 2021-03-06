# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client monolith-cian-announcementapi`

cian-codegen version: 1.15.0

"""
from dataclasses import dataclass
from typing import List, Optional

from cian_enum import NoFormat, StrEnum

from .agent_bonus import AgentBonus
from .utilities_terms import UtilitiesTerms


class ContractType(StrEnum):
    __value_format__ = NoFormat
    lease_assignment = 'leaseAssignment'
    """Переуступка прав аренды"""
    sale = 'sale'
    """Продажа"""


class Currency(StrEnum):
    __value_format__ = NoFormat
    eur = 'eur'
    """Евро"""
    rur = 'rur'
    """Рубль"""
    usd = 'usd'
    """Доллар"""


class IncludedOptions(StrEnum):
    __value_format__ = NoFormat
    operational_costs = 'operationalCosts'
    """Операционные расходы"""
    utility_charges = 'utilityCharges'
    """Коммунальные услуги"""


class LeaseTermType(StrEnum):
    __value_format__ = NoFormat
    few_months = 'fewMonths'
    """На несколько месяцев"""
    long_term = 'longTerm'
    """Длительный"""


class LeaseType(StrEnum):
    __value_format__ = NoFormat
    direct = 'direct'
    """Прямая аренда"""
    joint_venture = 'jointVenture'
    """Договор совместной деятельности"""
    sublease = 'sublease'
    """Субаренда"""


class PaymentPeriod(StrEnum):
    __value_format__ = NoFormat
    annual = 'annual'
    """За год"""
    monthly = 'monthly'
    """За месяц"""


class PriceType(StrEnum):
    __value_format__ = NoFormat
    all = 'all'
    """Цена за все"""
    square_meter = 'squareMeter'
    """Цена за квадратный метр"""
    sotka = 'sotka'
    """Сотка"""
    hectare = 'hectare'
    """Гектар"""


class SaleType(StrEnum):
    __value_format__ = NoFormat
    alternative = 'alternative'
    """Альтернатива"""
    dupt = 'dupt'
    """Договор уступки права требования"""
    dzhsk = 'dzhsk'
    """Договор ЖСК"""
    free = 'free'
    """Свободная продажа"""
    fz214 = 'fz214'
    """214-ФЗ"""
    investment = 'investment'
    """Договор инвестирования"""
    pdkp = 'pdkp'
    """Предварительный договор купли-продажи"""


class TenantsType(StrEnum):
    __value_format__ = NoFormat
    any = 'any'
    """Любой"""
    family = 'family'
    """Семья"""
    female = 'female'
    """Женщина"""
    male = 'male'
    """Мужчина"""


class VatType(StrEnum):
    __value_format__ = NoFormat
    included = 'included'
    """НДС включен"""
    not_included = 'notIncluded'
    """НДС не включен"""
    vat_included = 'vatIncluded'
    """НДС включен"""
    vat_not_included = 'vatNotIncluded'
    """НДС не включен"""
    usn = 'usn'
    """УСН (упрощенная система налогообложения)"""


@dataclass
class BargainTerms:
    price: Optional[float]  # не менять на float
    """Цена"""
    action_id: Optional[str] = None
    'Значение string.<br />\r\nВы можете добавить акцию, которая идет в вашем ЖК. Для этого вам необходимо обратиться к вашему курирующему менеджеру.\r\nId акции не ставится произвольно, вам его высылает менеджер.'
    agent_bonus: Optional[AgentBonus] = None
    """Бонус агенту"""
    agent_fee: Optional[int] = None
    """Комиссия от другого агента, %%. По умолчанию 100%."""
    bargain_allowed: Optional[bool] = None
    """Возможен торг"""
    bargain_conditions: Optional[str] = None
    """Условия торга"""
    bargain_price: Optional[float] = None
    """Цена с учетом торга"""
    client_fee: Optional[int] = None
    """Комиссия от прямого клиента, %%. По умолчанию 100%."""
    contract_type: Optional[ContractType] = None
    """Тип договора"""
    currency: Optional[Currency] = None
    """Валюта"""
    deposit: Optional[int] = None
    """Залог собственнику"""
    has_grace_period: Optional[bool] = None
    """Арендные каникулы"""
    included_options: Optional[List[IncludedOptions]] = None
    """Включено в ставку"""
    lease_term_type: Optional[LeaseTermType] = None
    """Срок аренды"""
    lease_type: Optional[LeaseType] = None
    """Тип аренды"""
    min_lease_term: Optional[int] = None
    """Минимальный срок аренды, мес"""
    mortgage_allowed: Optional[bool] = None
    """Ипотека"""
    payment_period: Optional[PaymentPeriod] = None
    """Период оплаты"""
    prepay_months: Optional[int] = None
    """Предоплата, от 1 до 12 месяцев"""
    price_for_workplace: Optional[int] = None
    """Цена за рабочее место в коворкинге."""
    price_type: Optional[PriceType] = None
    """Тип цены"""
    sale_type: Optional[SaleType] = None
    """Тип продажи"""
    security_deposit: Optional[int] = None
    """Обеспечительный платеж"""
    tenants_type: Optional[TenantsType] = None
    """Состав съемщиков"""
    utilities_terms: Optional[UtilitiesTerms] = None
    """Коммунальные услуги"""
    vat_included: Optional[bool] = None
    """НДС включен"""
    vat_price: Optional[float] = None
    vat_type: Optional[VatType] = None
