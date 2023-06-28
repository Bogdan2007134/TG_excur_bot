import asyncio

from aiogram import types, Dispatcher
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled
from aiogram.dispatcher.handler import CancelHandler, current_handler


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit: int = 0.7):
        BaseMiddleware.__init__(self)
        self.rate_limit = limit

    async def on_process_message(self, msg: types.Message, data: dict):
        dp = Dispatcher.get_current()

        try:
            await dp.throttle(key='antiflood_message', rate=self.rate_limit)
        except Throttled as _t:
            await self.msg_throttle(msg, _t)

            raise CancelHandler()

    async def msg_throttle(self, msg: types.Message, throttled: Throttled):
        delta = throttled.rate - throttled.delta
        if throttled.exceeded_count <= 2:
            await msg.reply(
                'Можно отправлять только 1 сообщениe в 0.5сек!!\nЕсли вы продолжите спамить,то я буду вынужден вас игнорировать!!')
            await asyncio.sleep(delta)
