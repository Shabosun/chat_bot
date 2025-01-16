from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup, 
    ReplyKeyboardRemove
)

reply_keyboard = [
    [
        InlineKeyboardButton("Заполнить анкету")
    ],
    [
        InlineKeyboardButton("Посмотреть список пользователей")
    ],
    [
        InlineKeyboardButton("Информация о боте")
    ]

]

questionnaire_keyboard = [
    [
        InlineKeyboardButton("Имя"),
        InlineKeyboardButton("Возраст")
    ],
    [
        InlineKeyboardButton("Пол"),
        InlineKeyboardButton("Хобби и интересы")
    ],
    [
        InlineKeyboardButton("Продолжить")
    ]

]

questionnaire_menu = ReplyKeyboardMarkup(keyboard=questionnaire_keyboard, resize_keyboard=True)
menu = ReplyKeyboardMarkup(keyboard=reply_keyboard, resize_keyboard=True)