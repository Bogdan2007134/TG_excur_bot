from aiogram.dispatcher.filters.state import StatesGroup, State

"""Состояния"""

class User(StatesGroup):
    dialog = State()


class UpdateExcur(StatesGroup):
    price = State()
    product_description = State()


class Mail(StatesGroup):
    mail = State()


class FeedbackState(StatesGroup):
    waiting_for_feedback = State()


class ExcurFeedbackState(StatesGroup):
    waiting_for_excur_feedback = State()


class UsersSupport(StatesGroup):
    id_support = State()
    usesname = State()
    response_text = State()


class ReviewForExcursions(StatesGroup):
    name = State()
    login = State()
    scores = State()
    excursus = State()
    feedback_text = State()


class PromocodeUser(StatesGroup):
    promocode = State()


class PromocodeAdmin(StatesGroup):
    promo = State()
    discount = State()
    usage = State()


class DELETEPromocodeAdmin(StatesGroup):
    promo_delete = State()
