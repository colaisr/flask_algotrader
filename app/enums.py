from enum import Enum


class Subscriptions(Enum):
    TRIAL = 1
    PERSONAL = 2
    CORPORATE = 3
    MANAGED_PORTFOLIO = 4


class UserRole(Enum):
    USER = 1
    ADMINISTRATOR = 2


class ProcessType(Enum):
    SPYDER = 1,
    NOTIFICATIONS = 2
