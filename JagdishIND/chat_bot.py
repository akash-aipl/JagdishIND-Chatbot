import re
import time
import logging
from telegram import KeyboardButton, Update
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler
from telegram.ext import Application, ContextTypes, MessageHandler, filters
from telegram import ForceReply, Update
from datetime import datetime, date
from telegram.ext import CallbackQueryHandler,ConversationHandler
from telegram import InlineKeyboardButton,InlineKeyboardMarkup
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

import pymongo

from options.nikol import nikol_vs
from options.other import other_vs

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["jbot"]

dblist = myclient.list_database_names()
collist = mydb.list_collection_names()

if "jbot" in dblist and "persons" in collist:
    print("* Database and collection is available *")
else:
    print("Database not found !")
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

FULLNAME ,DOB, MOBILE, WAPP, EMAIL, VOTER_ID, NIKOL_VS = range(7)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user
    currentTime = time.strftime('%H:%M')
    hour = datetime.now().hour
    userid = str(user.id)
    uid = userid.lstrip()

    dateTime = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    print(dateTime)

    chat_id=update.effective_chat.id
    print("Chat ID : ",chat_id)

    if chat_id == mydb.persons.find({"_id":uid}):
        print("Update Record")
        mydb.persons.update_one({"_id":uid},{"$set":{"DateTime":dateTime}})
    else:
        print("New Record")
        mydb.persons.update_one({"_id":uid},{"$set":{"_id":uid,"DateTime":dateTime}},upsert=True)
    
    if hour < 12 :
        await update.message.reply_html(
            rf"Hi.. {user.mention_html()}, Good Morning ",
        )
    
    if hour >= 12 and hour < 18:
        await update.message.reply_html(
            rf"Hi.. {user.mention_html()}, Good Afternoon",
        )
    if hour >= 18 :
        await update.message.reply_html(
            rf"Hi.. {user.mention_html()}, Good Evening",
        )

    await update.message.reply_html(
        rf"I'm JagdisHind Assistent."
    )

    """Starts the conversation and asks the user about their Full Name."""

    await update.message.reply_text(
        "May I know Your Full Name ?",
        reply_markup=ForceReply(selective=False),
    )
    return FULLNAME

async def fullname(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Stores the fullname."""
    user = update.message.from_user
    uid = str(user.id)
    logger.info("Full Name of %s: %s", user.first_name, update.message.text)
    mydb.persons.update_one({"_id":uid},{"$set":{"fullname":update.message.text}},upsert=True)
    await update.message.reply_text(
        "Can you tell me your Birth Date (DD-MM-YYYY) ?",
        reply_markup=ForceReply(selective=False),
    )
    return DOB

async def dob(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Stores the info about the user and ends the conversation."""
    user = update.message.from_user
    uid = str(user.id)
    date_object = datetime.strptime(update.message.text, "%d-%m-%Y")
    formatted_date = date_object.strftime("%d/%m/%Y")
    logger.info("DOB of %s: %s", user.first_name, formatted_date)
    mydb.persons.update_one({"_id":uid},{"$set":{"dob":formatted_date}},upsert=True)
    await update.message.reply_text(
        "Thank You. Can You Provide Your Mobile No ?",
        reply_markup=ForceReply(selective=False),
    )
    return MOBILE

async def mobile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Stores the info about the user and ends the conversation."""
    user = update.message.from_user
    r=re.fullmatch('[6-9][0-9]{9}',update.message.text)
    if r!=None:
        await update.message.reply_html(
            "Thank You. Can You Provide Your WhatsApp No ?",
            reply_markup=ForceReply(selective=False),
        )
    else:
        await update.message.reply_html(
            "Please provide a valid mobile number !",
            reply_markup=ForceReply(selective=False),
        )
        return MOBILE
    uid = str(user.id)
    logger.info("Mobile No of %s: %s", user.first_name, update.message.text)
    mydb.persons.update_one({"_id":uid},{"$set":{"mobile":update.message.text}},upsert=True)
    return WAPP

async def wapp(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Stores the user Whats App Number."""
    user = update.message.from_user
    r=re.fullmatch('[6-9][0-9]{9}',update.message.text)
    if r!=None:
        await update.message.reply_html(
            "Thank You. Can You Provide Your Email ID ?",
            reply_markup=ForceReply(selective=False),
        )
    else:
        await update.message.reply_html(
            "Please provide a valid WhatsApp number !",
            reply_markup=ForceReply(selective=False),
        )
        return WAPP
    uid = str(user.id)
    logger.info("WhatsApp No of %s: %s", user.first_name, update.message.text)
    mydb.persons.update_one({"_id":uid},{"$set":{"wapp_no":update.message.text}},upsert=True)
    return EMAIL

async def email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Stores the info about the user and ends the conversation."""
    user = update.message.from_user
    mpat = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if(re.fullmatch(mpat, update.message.text)):
        await update.message.reply_html(
            "Thank You !",
        )
    else:
        await update.message.reply_html(
            "Please provide a valid Email ID !",
            reply_markup=ForceReply(selective=False),
        )
        return EMAIL
    uid = str(user.id)
    logger.info("Email ID of %s: %s", user.first_name, update.message.text)
    mydb.persons.update_one({"_id":uid},{"$set":{"email":update.message.text}},upsert=True)

    keyboard = [
        [InlineKeyboardButton("નિકોલ વિધાનસભા", callback_data="1")],
        [InlineKeyboardButton("અન્ય", callback_data="2")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_html(
        rf"Please choose an Option",
        reply_markup=reply_markup
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
   
    user = update.effective_user  
    query = update.callback_query
    uid = str(user.id)
    await query.answer()
    button_choice=query.data
    print(type(button_choice))

    if button_choice=='1':
        mydb.gvpbot.update_one({"_id":uid},{"$set":{"nikol_vs":"true"}},upsert=True)
        await nikol_vs(update, context)
        voter_id = update.effective_message.text
        print(voter_id)
        mydb.persons.update_one({"_id":uid},{"$set":{"voter_id":voter_id}},upsert=True)
    if button_choice=='2':
        mydb.persons.update_one({"_id":uid},{"$set":{"other_vs":"true"}},upsert=True)
        await other_vs(update, context)

    if button_choice=='1.1':
        mydb.persons.update_one({"_id":uid},{"$set":{"mulakat":"true"}})
    if button_choice=='1.2':
        mydb.persons.update_one({"_id":uid},{"$set":{"rs_yojna":"true"}})

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

if __name__ == '__main__':
    application = ApplicationBuilder().token('5547103630:AAFafbPlUAPFcr3tCdhkdYQpJd8V23SPIB0').build()
    
    # Add conversation handler with the states Fullname, DOB, Email and Phone
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            FULLNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, fullname)],
            DOB: [MessageHandler(filters.TEXT & ~filters.COMMAND, dob)],
            MOBILE:  [MessageHandler(filters.TEXT & ~filters.COMMAND, mobile)],
            WAPP:  [MessageHandler(filters.TEXT & ~filters.COMMAND, wapp)],
            EMAIL:  [MessageHandler(filters.TEXT & ~filters.COMMAND, email)],
            # NIKOL_VS : [MessageHandler(filters.TEXT & ~filters.COMMAND, nikol_vs(Update, ContextTypes.DEFAULT_TYPE))],
            # VOTER_ID:  [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_voter_id)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(CallbackQueryHandler(button))

    application.add_handler(conv_handler)

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,reply))
    
    application.run_polling()
