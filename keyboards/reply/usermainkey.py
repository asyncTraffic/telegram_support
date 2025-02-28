from aiogram.types import *


kb = [
        [
            KeyboardButton(text="📄 Частые вопросы"),
        ]
    ]
menuReply = ReplyKeyboardMarkup(
    keyboard=kb,
    resize_keyboard=True,
    input_field_placeholder="Задай свой вопрос!"
)

