import logging

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

# if __version_info__ < (20, 0, 0, "alpha", 1):
#     raise RuntimeError(
#         f"This example is not compatible with your current PTB version {TG_VER}. To view the "
#         f"{TG_VER} version of this example, "
#         f"visit https://github.com/python-telegram-bot/python-telegram-bot/tree/v{TG_VER}/examples"
#     )
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters


async def eg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Prompt same text & keyboard as `start` does but not as new message"""
    # Get CallbackQuery from Update
    # query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    # await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("About Us", callback_data='1.1')
        ],
        [
            InlineKeyboardButton("Academic Program", callback_data='1.2'),
            InlineKeyboardButton("Administration", callback_data='1.3')
        ],
        [
            InlineKeyboardButton("Library", callback_data='1.4'),
            InlineKeyboardButton("Sports", callback_data='1.5')
        ],
        [
            InlineKeyboardButton("Upcoming Program", callback_data='1.6'),
            InlineKeyboardButton("Rural Center", callback_data='1.7')
        ],
        [
            InlineKeyboardButton("Krishi Vigyan Kendra", callback_data='1.8'),
            InlineKeyboardButton("Museum", callback_data='1.9')
        ],
        [
            InlineKeyboardButton("Heritage Walk", callback_data='1.10')
        ],
        [
            InlineKeyboardButton("Back", callback_data='0')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # await update.message.reply_text("Start handler, Choose a route", reply_markup=reply_markup)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="ENGLISH LANGUAGE",reply_markup=reply_markup)



async def other_vs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass