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

from database.controller import ChatDB

CHOOSING, USERS, MENU, TYPING_REPLY, TYPING_CHOICE  = range(5)


filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)


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
    await update.message.reply_text(f"Your {text.lower()}? Yes, I would love to hear about that!")

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
    
    
async def print_users(update : Update, context : ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Пользователи: ")

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
    return ConversationHandler.END
    



def main() -> None:

    try:
        persistance = PicklePersistence(filepath="conversationbot")
        application = Application.builder().token(config.TOKEN).persistence(persistance).build()

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
                MENU: [
                ],
                USERS:[
                    
                ]
            },
            fallbacks = [
                CommandHandler("start", start),
                MessageHandler(filters.Regex("^Продолжить$"), done),
                MessageHandler(filters.Regex("Посмотреть список пользователей"), print_users),
                MessageHandler(filters.Regex("Информация о боте"), print_bot_info),
                
            ],
            name="chat_bot",
            persistent=True
            
        )

        application.add_handler(conv_handler)


        application.run_polling()
    except Exception as ex:
        print(ex)




if __name__ == "__main__":
    logger.info("Starting...")
    main()
