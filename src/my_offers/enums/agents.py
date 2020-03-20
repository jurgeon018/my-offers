from cian_enum import NoFormat, StrEnum


class AgentAccountType(StrEnum):
    __value_format__ = NoFormat

    specialist = 'Specialist'
    """Специалист"""
    agency = 'Agency'
    """Агентство"""
    management_company = 'ManagementCompany'
    """Управляющая компания"""
    rent_department = 'RentDepartment'
    """Отдел аренды"""
