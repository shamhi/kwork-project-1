from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_i18n import I18nContext

from app.data_structures.cd import LanguageCD, ContractCD
from app.data_structures.enums import Lang, ContractStatus


def get_start_kb(i18n: I18nContext):
    builder = InlineKeyboardBuilder()
    builder.button(text=i18n.get('start-user-ru-button-text'), callback_data=LanguageCD(language=Lang.RU))
    builder.button(text=i18n.get('start-user-kk-button-text'), callback_data=LanguageCD(language=Lang.KK))
    builder.adjust(1)
    return builder.as_markup()


def get_start_work_kb(i18n: I18nContext):
    builder = InlineKeyboardBuilder()
    builder.button(text=i18n.get('start-work-with-us-button-text'), callback_data='start-work')
    return builder.as_markup()


def get_contract_kb(i18n: I18nContext):
    builder = InlineKeyboardBuilder()
    builder.button(text=i18n.get('contract-accept-button-text'),
                   callback_data=ContractCD(status=ContractStatus.WAIT))
    builder.button(text=i18n.get('contract-decline-button-text'),
                   callback_data=ContractCD(status=ContractStatus.DECLINE))
    builder.adjust(1)
    return builder.as_markup()


def get_sure_contract_kb(i18n: I18nContext):
    builder = InlineKeyboardBuilder()
    builder.button(text=i18n.get('contract-sure-accept-button-text'),
                   callback_data=ContractCD(status=ContractStatus.ACCEPT))
    builder.button(text=i18n.get('contract-decline-button-text'),
                   callback_data=ContractCD(status=ContractStatus.DECLINE))
    builder.adjust(1)
    return builder.as_markup()
