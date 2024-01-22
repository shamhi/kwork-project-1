from enum import Enum


class Lang(Enum):
    RU = "RU"
    KK = "KK"

class ContractStatus(Enum):
    ACCEPT = 'A'
    DECLINE = 'D'
    WAIT = 'W'
