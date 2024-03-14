# Import required classes from the library
import os, re
from telegram.ext import ContextTypes
from datetime import datetime
from telegram.constants import ParseMode

def escape_special_characters(text):
    # Define the pattern for special characters that need to be escaped
    pattern = r'(\\|\[|\]|\(|\)|~|>|#|\+|-|=|\||\{|\}|\.|!)'
    
    # Use the sub method from re to replace the characters with their escaped versions
    escaped_text = re.sub(pattern, r'\\\1', text)
    
    return escaped_text

# Admin Notify Function
async def admin_notify(context: ContextTypes.DEFAULT_TYPE, admin_chat_id: int, user_chat_id: int, rquest_type:str, user_input: str, result_code: str) -> None:
    # Get today's date in the format YYYY-MM-DD
    today_date = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

    # Define the error message for amdin and maintain the bot
    stats_message = (f'⏰ Time: {today_date}\n'
                     f'🧍‍♂ User: {user_chat_id}\n'
                     f'🧍‍♂ Request: {rquest_type}\n'
                     f'📤 User input: {escape_special_characters(user_input)}\n'
                     f'🧨 Result: `{result_code}`')
    
    # Send the error message to admin
    await context.bot.send_message(
            text= stats_message, 
            chat_id=admin_chat_id,
            parse_mode=ParseMode.MARKDOWN_V2
        )

# AIRM Auditor bot log function
def log_function(chat_id, request_type, user_input, result):
    log_path = "log.txt"
    time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    print(f'{time}--------{chat_id}--------{request_type}--------{user_input}--------{result}')
    with open(log_path, 'a+', encoding='utf-8') as f:
        f.write(f'{time}--------{chat_id}--------{request_type}--------{user_input}--------{result}\n')
        f.close()