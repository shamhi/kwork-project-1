from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram_i18n import I18nContext


def get_cities_kb():
    cities_list = ['Астана', 'Алматы', 'Шымкент']  # Брать с базы данных
    builder = ReplyKeyboardBuilder()
    for city in cities_list:
        builder.button(text=city)

    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def get_phone_number(i18n: I18nContext):
    builder = ReplyKeyboardBuilder()
    builder.button(text=i18n.get('ask-share-phone-button-text'), request_contact=True)
    return builder.as_markup(resize_keyboard=True)
