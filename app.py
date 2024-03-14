# Import required classes from the library
import os, requests
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from dotenv import load_dotenv

from src.main.stactic_commands import *
from src.main.handle_callback import *
# from src.main.user_settings import *
from src.main.main_commands import *

load_dotenv(dotenv_path='.env')

# Use your own bot token here
TOKEN = os.getenv('TG_TOKEN')
API_URL = f"https://api.telegram.org/bot{TOKEN}/setMyCommands"

commands = [
    {"command": "start", "description": "Displays help text"},
    {"command": "image", "description": "Generate image."},
    {"command": "ximage", "description": "Process the image."},
    {"command": "web", "description": "Web AI Questions."},
    {"command": "web_summary", "description": "Web AI Summary Agent"},
    {"command": "help", "description": "How to use the bot"},
    {"command": "stats", "description": "Displays the bot stats"}
]

response = requests.post(API_URL, json={"commands": commands})

# Main function update
def main() -> None:
    application = Application.builder().token(TOKEN).build()
    
    # Existing /start handler
    start_handler = CommandHandler('start', bot_start)
    application.add_handler(start_handler)

    stats_handler = CommandHandler('stats', stats)
    application.add_handler(stats_handler)

    help_handler = CommandHandler('help', help)
    application.add_handler(help_handler)

    # Add the /image command handler to the application
    image_handler = CommandHandler('image', image_handle)
    application.add_handler(image_handler)

    # Add the /ximage command handler to the application
    ximage_handler = CommandHandler('ximage', ximage_handle)
    application.add_handler(ximage_handler)

    # Add the /web command handler to the application
    url_handler = CommandHandler('web', web_handle)
    application.add_handler(url_handler)

    # Add the /web_summary command handler to the application
    web_summary_handler = CommandHandler('web_summary', web_summary_handle)
    application.add_handler(web_summary_handler)

    general_iamge_handler = MessageHandler(filters.PHOTO, general_image_handle)
    application.add_handler(general_iamge_handler)

    general_handler = MessageHandler(filters=filters.TEXT, callback=general_chat_handle)
    application.add_handler(general_handler)
    # Add the CallbackQueryHandler with a different variable name to avoid conflict
    callback_query_handler_obj = CallbackQueryHandler(callback_query_handler)
    application.add_handler(callback_query_handler_obj)
    
    application.run_polling()

if __name__ == '__main__':
    main()