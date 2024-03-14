# Import required classes from the library
import json
from telegram.ext import ContextTypes
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime
from telegram.constants import ParseMode
from ..model.crud import get_user_by_id, create_user, count_groups, count_individual_user

# Define the start command callback function
async def bot_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Define the response message and buttons
    chat_id = update.message.chat_id
    if not get_user_by_id(chat_id):
        create_user(chat_id)
    keyboard = [[
        InlineKeyboardButton("➕ Add me to your group", url="https://t.me/"),
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Welcome aboard!\n"
        "Introducing Telegram's AI Chatbot.\n\n"
        "🎨 Generate an image from text in seconds\n"
        "🎇 Process the image and answer about the picture\n"
        "🌐 Answers to the questions about the web 🔍\n"
        "🌐 Summarize the website 🖊\n", reply_markup=reply_markup
    )

# Define the stats command callback function
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Get today's date in the format YYYY-MM-DD
    today_date = datetime.now().strftime("%Y-%m-%d")
    user_count = count_individual_user()
    group_count = count_groups()

    with open("log.txt", 'r', encoding='utf-8') as f:
        imporession_count = len(f.readlines())
        f.close()
    # Define the stats message with the current date
    stats_message = (f'📊 *AIRM Chatbot stats for {today_date}:*\n\n'
                     f'💬 Groups using AIRM Auditor Bot: *{group_count}*\n'
                     f'👤 Unique users: *{user_count}*\n'
                     f'👁️ User impressions: *{imporession_count}*')
    # Send the stats message
    await update.message.reply_text(stats_message, parse_mode=ParseMode.MARKDOWN)

# Define the help command callback function
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        """🦾 How to use the bot

🎨 image command
The <code>/image</code> command generates image from text.

🎇 ximage command
The <code>/ximage</code> command processes images. This commands answer questions about or describe an image. When sending an image, you must include a question as a caption.

🌐 web
The <code>/web</code> command answers question about the website.

🌐 web_summary
The <code>/web_summary</code> command summarizes the website.

🍀 P.S. Using bot in group
In group, many people chat with each other. So to use bot in group, you need to nter Bot Name. Please enter the bot name first, followed by your input text.
E.g. <code>@AIRMChatBOT https://www.airealm.tech/</code>, <code>@AIRMChatBOT What is contract address of this</code>"""
    )
    await update.message.reply_text(help_text, disable_web_page_preview=True, parse_mode=ParseMode.HTML)