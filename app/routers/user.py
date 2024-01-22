from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram_i18n import I18nContext
import aiosqlite

from app.keyboards import ikb, rkb
from app.states import SendCode
from app.data_structures.cd import LanguageCD, ContractCD
from app.data_structures.enums import ContractStatus
from app.utils import scripts
from app.db import Database

user = Router(name=__name__)


@user.message(CommandStart(), StateFilter(None))
async def cmd_start(message: Message, i18n: I18nContext, conn: aiosqlite.Connection):
    db = Database(connection=conn)

    await db.create_users_table()
    await db.register_user(user_id=message.from_user.id, name=message.from_user.first_name)

    await message.answer(i18n.get('start-user-text'), reply_markup=ikb.get_start_kb(i18n=i18n))


@user.message(Command('cancel'))
async def cmd_cancel(message: Message, i18n: I18nContext, state: FSMContext):
    await message.answer(text=i18n.get('cancel-text'))
    await state.clear()


@user.callback_query(LanguageCD.filter())
async def change_language(call: CallbackQuery, i18n: I18nContext, callback_data: LanguageCD):
    lang = callback_data.language.value.lower()
    await i18n.set_locale(lang)

    await call.message.edit_text(text=i18n.get('start-work-with-us-text'),
                                 reply_markup=ikb.get_start_work_kb(i18n=i18n))


@user.callback_query(F.data == 'start-work')
async def ask_contract(call: CallbackQuery, i18n: I18nContext, state: FSMContext):
    await call.message.edit_text(text=i18n.get('ask-contract-text'), reply_markup=ikb.get_contract_kb(i18n=i18n))

    await state.set_state(SendCode.agreement)


@user.callback_query(ContractCD.filter(F.status == ContractStatus.WAIT), StateFilter(SendCode.agreement))
async def ask_sure_contract(call: CallbackQuery, i18n: I18nContext, callback_data: ContractCD):
    await call.message.edit_text(text=i18n.get('ask-contract-sure-accept-text'),
                                 reply_markup=ikb.get_sure_contract_kb(i18n=i18n))


@user.callback_query(ContractCD.filter(F.status == ContractStatus.ACCEPT), StateFilter(SendCode.agreement))
async def accept_contract(call: CallbackQuery, i18n: I18nContext, callback_data: ContractCD, state: FSMContext):
    await call.message.delete()
    await call.message.answer(text=i18n.get('ask-city-text'), reply_markup=rkb.get_cities_kb())

    await state.set_state(SendCode.city)


@user.callback_query(ContractCD.filter(F.status == ContractStatus.DECLINE), StateFilter(SendCode.agreement))
async def decline_contract(call: CallbackQuery, i18n: I18nContext, callback_data: ContractCD, state: FSMContext):
    await call.message.delete()
    await call.message.answer(text=i18n.get('contract-decline-text'))

    await state.clear()


@user.message(F.text.regexp(r"^[a-zA-Zа-яА-Я]+$"), StateFilter(SendCode.city))
async def ask_phone_number(message: Message, i18n: I18nContext, state: FSMContext):
    await message.answer(text=i18n.get('ask-share-phone-text'), reply_markup=rkb.get_phone_number(i18n=i18n))

    await state.update_data(city=message.text)
    await state.set_state(SendCode.phone)


@user.message(F.text, StateFilter(SendCode.city))
async def wrong_city_type(message: Message, i18n: I18nContext):
    await message.answer(text=i18n.get('wrong-city-type-text'))


@user.message(F.contact, StateFilter(SendCode.phone))
async def send_code(message: Message, i18n: I18nContext, state: FSMContext, conn: aiosqlite.Connection):
    db = Database(connection=conn)
    state_data = await state.get_data()

    user_id = message.from_user.id
    phone = message.contact.phone_number
    city = state_data.get('city')

    await db.insert_city(city=city, user_id=user_id)
    await db.insert_phone(user_id=user_id, phone=phone)
    check_code = await db.check_code(user_id=user_id)

    if check_code:
        return await message.answer(text=i18n.get('send-old-code-text', code=check_code),
                                    reply_markup=ReplyKeyboardRemove())

    all_codes = await db.get_all_codes()
    code = scripts.get_unique_code(all_codes)

    await db.insert_code(user_id=user_id, code=code)

    await message.answer(text=i18n.get('send-new-code-text', code=code), reply_markup=ReplyKeyboardRemove())

    await state.clear()
