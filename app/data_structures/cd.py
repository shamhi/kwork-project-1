from aiogram.filters.callback_data import CallbackData

from app.data_structures.enums import Lang, ContractStatus


class LanguageCD(CallbackData, prefix="lang"):
    language: Lang


class ContractCD(CallbackData, prefix='contract'):
    status: ContractStatus
