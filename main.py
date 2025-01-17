import config
from logger import logger
from markups import menu, questionnaire_menu

from warnings import filterwarnings
from telegram.warnings import PTBUserWarning

from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    LinkPreviewOptions,
    ReplyKeyboardRemove
)

from telegram.ext import (
    ContextTypes, 
    PicklePersistence,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    filters,
    Application,
    TypeHandler,
    CallbackQueryHandler,
    PreCheckoutQueryHandler,
    CallbackContext
)

from database.controller import db


CHOOSING, USERS, MENU, TYPING_REPLY, TYPING_CHOICE, CHATTING  = range(6)


filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)

def users_to_str_users_list():
    users = db.get_all_users()
    users_list = []
    for user in users:
        users_list.append(f"""{user.username}, {user.age} 
        \n{user.tg_name}
        \n{user.info}""")
    return users_list



# items = [f"Item {i}" for i in range(1, 101)] 
# items = users_to_str()
# items_per_page = 1


async def start(update : Update, context : ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user
    reply_text = f"""Привет, {user.name}, я твой бот-помощник в поиске друзей! 
    \nТы можешь выбрать действие с помощью меню ниже!
    \nНо для начала давай заполним анкету :)"""

    await update.message.reply_text(reply_text, reply_markup=questionnaire_menu)

    return CHOOSING


def facts_to_str(user_data: dict[str, str]) -> str:
    """Helper function for formatting the gathered user info."""
    facts = [f"{key} - {value}" for key, value in user_data.items()]
    return "\n".join(facts).join(["\n", "\n"])

async def regular_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    context.user_data["choice"] = text
    await update.message.reply_text(f"{text.lower()}? Да, я бы с удовольствием об этом услышал!")

    return TYPING_REPLY


async def received_information(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Store info provided by user and ask for the next category."""
    user_data = context.user_data
    text = update.message.text
    category = user_data["choice"]
    user_data[category] = text
    del user_data["choice"]

    await update.message.reply_text(
        "Вот, что я уже знаю о тебе:"
        f"{facts_to_str(user_data)}",
        reply_markup=questionnaire_menu
    )

    return CHOOSING
    
async def print_bot_info(update : Update, context : ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        """Данный телеграм бот предназначен для подростков, которым не хватает компании или друзей для общения. Бот поможет найти единомышленников, с которыми можно пообщаться, погулять или провести время.
    Чтобы начать использовать бота, пользователю необходимо зарегистрироваться и заполнить анкету с информацией о себе: возраст, пол, увлечения, хобби и т.д.
    После заполнения анкеты бот предложит подобрать подходящих собеседников по интересам и предпочтениям. Пользователь сможет начать общение с новыми друзьями и находить компанию для различных мероприятий.
    Такой телеграм бот поможет подросткам расширить круг общения, найти новых друзей и проводить время с интересными людьми, что способствует развитию социальных навыков и общению.
      Не забывай что люди могут выдовать себя за других!!!"""
    )


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display the gathered info and end the conversation."""
    user_data = context.user_data
    if "choice" in user_data:
        del user_data["choice"]

    await update.message.reply_text(
        f"Вот твоя анкета: {facts_to_str(user_data)} Давай продолжим!",
        reply_markup=menu,
    )

    user_data.clear()
    # return ConversationHandler.END
    return USERS
    

async def print_users(update: Update, context: CallbackContext) -> int:
    """Отправляет первое сообщение с кнопками пагинации."""
    context.user_data['page'] = 0  # Начинаем с первой страницы
    await send_page(update, context)
    # await update.message.reply_text("users_list")
    return MENU

async def send_page(update: Update, context: CallbackContext) -> None:
    """Отправляет сообщение с элементами текущей страницы."""


    items = users_to_str_users_list()
    # usrs = db.get_all_users()
    items_per_page = 1
    
    page = context.user_data['page']
    start_index = page * items_per_page
    end_index = start_index + items_per_page
    page_items = items[start_index:end_index]
    
    

    message = "\n".join(page_items)
    # message = users_to_str_users_list()
    # message = db.user_to_str(page_items[page])
    
    keyboard = []
    # Кнопки "Назад" и "Вперед"
    if page > 0:
        keyboard = [
            [
                # InlineKeyboardButton("Написать анонимно", callback_data='hello')
                InlineKeyboardButton("Написать анонимно", callback_data=context.user_data['page'])
            ],
            [
                InlineKeyboardButton("Назад", callback_data='prev'),
                InlineKeyboardButton("Вперед", callback_data='next')

            ]
        ]
        
    if end_index < len(items):
        keyboard = [
            [
                #InlineKeyboardButton("Написать анонимно", callback_data='hello')
                InlineKeyboardButton("Написать анонимно", callback_data=context.user_data['page'])
                
            ],
            [
                InlineKeyboardButton("Назад", callback_data='prev'),
                InlineKeyboardButton("Вперед", callback_data='next')

            ]
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if page == 0:
        await update.message.reply_text(message, reply_markup=reply_markup)
    else:
        await update.message.edit_text(message, reply_markup=reply_markup)
    
    # await update.message.reply_text(message, reply_markup=reply_markup)

async def button(update: Update, context: CallbackContext) -> None:
    """Обрабатывает нажатия кнопок."""
    query = update.callback_query
    query.answer()
   
   

    if query.data == 'prev':
        context.user_data['page'] -= 1
        print('prev')
    elif query.data == 'next':
        print("next")
        context.user_data['page'] += 1
    else:
        print("smth")
        user_id = int(query.data) + 1
        companion = db.get_user_by_id()
        
        # print(context.user_data['page'])
        # user_id = context.user_data['page'] + 1
        # user = db.get_user_by_id(user_id)
        # print(user.username)
    

    await send_page(query, context)


def main() -> None:

    try:
        # persistance = PicklePersistence(filepath="conversationbot")
        application = (Application
                       .builder()
                       .token(config.TOKEN)
                       #.persistence(persistance)
                       .build())

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler("start", start)],
            states={
                CHOOSING: [
                    MessageHandler(
                    filters.Regex("^(Имя|Возраст|Пол|Хобби и интересы)$"), regular_choice),
                    # MessageHandler(filters.Regex("Заполнить анкету"), regular_choice)

                    
                ],
                TYPING_CHOICE: [
                     MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Продолжить$")), regular_choice
                )
                ],
                TYPING_REPLY:[
                    MessageHandler(filters.TEXT & ~(filters.COMMAND | filters.Regex("^Продолжить$")), received_information)
                ],
                USERS:[
                    MessageHandler(filters.Regex("^Посмотреть список пользователей$"), print_users),
                    # CallbackQueryHandler(button),
                    # CallbackQueryHandler(show_profile, pattern="^hello$")
                    
                ],
                MENU: [
                        # CallbackQueryHandler(button, pattern="^prev|next|hello$"),
                        CallbackQueryHandler(button)
                ],
                CHATTING: [

                ]
            },
            fallbacks = [
                CommandHandler("start", start),
                MessageHandler(filters.Regex("^Продолжить$"), done),
                # MessageHandler(filters.Regex("Посмотреть список пользователей"), print_users),
                MessageHandler(filters.Regex("Информация о боте"), print_bot_info),
                
            ],
            name="chat_bot",
            # persistent=True
            
        )

        application.add_handler(conv_handler)


        application.run_polling()
    except Exception as ex:
        print(ex)




if __name__ == "__main__":
    logger.info("Starting...")
    main()
