from aiogram.types import *

kbMainAdmin = [
        [
            KeyboardButton(text="📢 Рассылка"),
            KeyboardButton(text="👤 Клиенты"),
        ],
        [
            KeyboardButton(text="⚙️ Настройки"),
        ],
    ]

keyReplayAdmin = ReplyKeyboardMarkup(
    keyboard=kbMainAdmin,
    resize_keyboard=True,
    input_field_placeholder="Действуйте!"
)

kbSetting= [
    [
        KeyboardButton(text="↩️ Назад")
    ],
    [
        KeyboardButton(text="✍🏻 Приветствие"),
        KeyboardButton(text="✍🏻 FAQ"),
    ],
    [
        KeyboardButton(text="🔧 Работа бота"),
        KeyboardButton(text="💭 Чат")
    ]
]

keySettingsAdmin = ReplyKeyboardMarkup(
    keyboard=kbSetting,
    resize_keyboard=True,
    input_field_placeholder="Действуйте!"
)