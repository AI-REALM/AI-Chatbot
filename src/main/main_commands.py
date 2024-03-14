# Import required classes from the library
import asyncio, os, re
from telegram.ext import ContextTypes
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from ..model.crud import get_user_by_id, create_user, update_moethod, update_url
from ..features.image_processing import image_description, image_generation
from ..features.web_questions import answer_website
from .admin_commands import admin_notify, log_function
from dotenv import load_dotenv
load_dotenv(dotenv_path='.env')

admin = int(os.getenv('ADMIN'))

def escape_special_characters(text):
    # Define the pattern for special characters that need to be escaped
    pattern = r'(\\|\[|\]|\(|\)|~|>|#|\+|-|=|\||\{|\}|\.|!)'
    
    # Use the sub method from re to replace the characters with their escaped versions
    escaped_text = re.sub(pattern, r'\\\1', text)
    
    return escaped_text

# /ximage handling functions
async def processing_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Define the response message and buttons
    message = update.message or update.callback_query.message
    # Download file
    new_file = await message.effective_attachment[-1].get_file()
    prompt = update.message.caption

    if prompt:
        pass
    else:
        prompt = "Explain about this image"

    sent_message = await message.reply_text(f'Image processing ...', parse_mode=ParseMode.MARKDOWN)

    # image processing
    description, code = image_description(image_url=new_file.file_path, prompt=prompt)
    if description:
        log_function(chat_id=message.chat_id, request_type="processing", user_input=f'{new_file.file_path} ---- {prompt}', result="successful")
        await sent_message.delete()
        await context.bot.send_message(
            text= f'{escape_special_characters(description)}', 
            chat_id=message.chat_id,
            parse_mode=ParseMode.MARKDOWN_V2
        )
    else:
        log_function(chat_id=message.chat_id, request_type="processing", user_input=f'{new_file.file_path}-----{prompt}', result=code)
        await admin_notify(context=context, admin_chat_id=admin, user_chat_id=message.chat_id, rquest_type="processing", user_input=f'{new_file.file_path}-----{prompt}', result_code=code)
        await sent_message.edit_text(f'❌ Failed in the generation of your pictures. Please retry after a few minutes.\nP.S. If you want to know more details, please contact me directly @fieryfox617',parse_mode=ParseMode.MARKDOWN)
        await asyncio.sleep(5)
        await sent_message.delete()

# /ximage handling functions
async def ximage_handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Define the response message and buttons
    message = update.message or update.callback_query.message
    chat_id = message.chat_id
    user = get_user_by_id(chat_id)
    # Check current user default method and update the method
    if not user:
        create_user(chat_id)
    if user.method != "processing":
        update_moethod(user.id, "processing")

    await message.reply_text(f'Please send me an image and your question as a caption.', parse_mode=ParseMode.MARKDOWN)

# /image handling functions
async def generation_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Define the response message and buttons
    message = update.message or update.callback_query.message

    text = update.message.text or update.callback_query.data
    if "@AIRMAuditorBOT" in text:
        text = text.replace("@AIRMAuditorBOT", "").strip()

    sent_message = await message.reply_text(f'Generating image ...', parse_mode=ParseMode.MARKDOWN)

    # image processing
    description, code = image_generation(prompt=text)
    if description:
        log_function(chat_id=message.chat_id, request_type="generation", user_input=text, result="successful")
        await sent_message.delete()
        await context.bot.send_photo(
            photo=description,
            chat_id=message.chat_id,
            parse_mode=ParseMode.MARKDOWN_V2
        )
    else:
        log_function(chat_id=message.chat_id, request_type="generation", user_input=text, result=code)
        await admin_notify(context=context, admin_chat_id=admin, user_chat_id=message.chat_id,rquest_type="generation", user_input=text, result_code=code)
        await sent_message.edit_text(f'❌ Failed in the generation of your pictures. Please retry after a few minutes.\nP.S. If you want to know more details, please contact me directly @fieryfox617',parse_mode=ParseMode.MARKDOWN)
        await asyncio.sleep(5)
        await sent_message.delete()

# /image handling functions
async def image_handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Define the response message and buttons
    message = update.message or update.callback_query.message
    chat_id = message.chat_id
    user = get_user_by_id(chat_id)
    # Check current user default method and update the method
    if not user:
        create_user(chat_id)
    if user.method != "generation":
        update_moethod(user.id, "generation")

    await message.reply_text(f'Send the image description is the next message, e.g. \'cat\'', parse_mode=ParseMode.MARKDOWN)

# /web handling functions
async def web_question(update: Update, context: ContextTypes.DEFAULT_TYPE, url:str, question:str) -> None:
    # Define the response message and buttons
    message = update.message or update.callback_query.message

    sent_message = await message.reply_text(f'Please wait for a moment. Let me think about it...', parse_mode=ParseMode.MARKDOWN)

    # image processing
    answer, code = answer_website(url=url, question=question)
    if answer:
        log_function(chat_id=message.chat_id, request_type="web", user_input=f'{url} --- {question}', result="successful")
        r_answer = escape_special_characters(answer)
        await sent_message.delete()
        await context.bot.send_message(
            text= r_answer, 
            chat_id=message.chat_id,
            parse_mode=ParseMode.MARKDOWN_V2
        )
    else:
        log_function(chat_id=message.chat_id, request_type="web", user_input=f'{url} --- {question}', result=code)
        await admin_notify(context=context, admin_chat_id=admin, user_chat_id=message.chat_id, rquest_type="generation", user_input=f'{url} --- {question}', result_code=code)
        if code == "Scrapping_failed":
            await sent_message.edit_text(f'🔍 The content for the provided URL cannot be retrieved. This could be due to the website being inaccessible or having anti-bot protection.\nIf you have any other questions about AIgentX, please contact me directly @fieryfox617.', parse_mode=ParseMode.MARKDOWN)
        else:
            await sent_message.edit_text(f'The provided source of information does not answer your question, please rephrase it. If you have any questions, please contact me directly @fieryfox617.',parse_mode=ParseMode.MARKDOWN)
        await asyncio.sleep(5)
        await sent_message.delete()

# /web handling functions
async def web_handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Define the response message and buttons
    message = update.message or update.callback_query.message
    chat_id = message.chat_id
    user = get_user_by_id(chat_id)
    # Check current user default method and update the method
    if not user:
        create_user(chat_id)
    if user.method != "weburl":
        update_moethod(user.id, "weburl")

    await message.reply_text(f'Please provide the URL of the webpage you want to ask about.', parse_mode=ParseMode.MARKDOWN)

# /web_summary handling functions
async def web_summary_handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Define the response message and buttons
    message = update.message or update.callback_query.message
    chat_id = message.chat_id
    user = get_user_by_id(chat_id)
    # Check current user default method and update the method
    if not user:
        create_user(chat_id)
    if user.method != "websummary":
        update_moethod(user.id, "websummary")

    await message.reply_text(f'Please provide the URL of the webpage you want summarized.', parse_mode=ParseMode.MARKDOWN)

# general image handler function
async def general_image_handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message or update.callback_query.message
    # text = update.message.text or update.callback_query.data
    # if "@AIRMAuditorBOT" in text:
    #     text = text.replace("@AIRMAuditorBOT", "").strip()
    
    chat_id = message.chat_id
    user = get_user_by_id(chat_id)
    if not user:
        create_user(chat_id)
    
    if user.method == "processing":
        await processing_image(update=update, context=context)

# general chat handler function
async def general_chat_handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message or update.callback_query.message
        
    chat_id = message.chat_id
    user = get_user_by_id(chat_id)
    if not user:
        create_user(chat_id)
    
    if user.method == "generation":
        await generation_image(update=update, context=context)

    elif user.method == "web":
        text = update.message.text or update.callback_query.data
        if "@AIRMAuditorBOT" in text:
            text = text.replace("@AIRMAuditorBOT", "").strip()
        await web_question(update=update, context=context, url=user.url, question=text)

    elif user.method == "weburl":
        update_moethod(user.id, "web")
        text = update.message.text or update.callback_query.data
        if "@AIRMAuditorBOT" in text:
            text = text.replace("@AIRMAuditorBOT", "").strip()
        update_url(id=user.id, url=text)
        await message.reply_text(f'What is your question about this website?', parse_mode=ParseMode.MARKDOWN)

    elif user.method == "websummary":
        update_moethod(user.id, "websummary")
        text = update.message.text or update.callback_query.data
        if "@AIRMAuditorBOT" in text:
            text = text.replace("@AIRMAuditorBOT", "").strip()

        await web_question(update=update, context=context, url=text, question="Write about this summary")


