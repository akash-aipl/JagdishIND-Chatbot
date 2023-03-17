import logging
import pymongo
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ForceReply
from telegram.ext import ContextTypes, CallbackContext
from telegram import __version__ as TG_VER

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["jbot"]

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

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

async def nikol_vs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_html(
        rf"Please enter your Voter IDthen select an option",
        reply_markup=ForceReply(selective=False)
    )
    await handle_voter_id(update, context)

async def handle_voter_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    uid = str(user.id)
    # voter_id = update.effective_message.text
    # print(voter_id)
    # mydb.persons.update_one({"_id":uid},{"$set":{"voter_id":voter_id}},upsert=True)

    keyboard = [
        [InlineKeyboardButton("મુલાકાત", callback_data="1.1")],
        [InlineKeyboardButton("રાજ્ય સહકારી યોજના", callback_data="1.2")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.effective_message.reply_html(
        rf"Please Choose an Option",
        reply_markup=reply_markup
    )