import os
import logging
import sqlitecloud
import httpx
from telegram import Update, InlineQueryResultPhoto, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, filters, InlineQueryHandler, ContextTypes, CallbackContext
from rembg import remove
from io import BytesIO
from PIL import Image
import numpy as np
from dotenv import load_dotenv
import datetime
import random
import string
import json

def handler(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Hello, World!'})
    }


# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME")
CHANNEL_PRIVATE_LINK = os.getenv("CHANNEL_PRIVATE_LINK")
API_KEY = os.getenv("API_KEY")

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Database connection
def create_connection():
    try:
        conn = sqlitecloud.connect(f"sqlitecloud://cgsefktrsz.sqlite.cloud:8860?apikey={API_KEY}")
        conn.execute("USE DATABASE users.db")
        return conn
    except Exception as e:
        logger.error(f"Error creating connection to SQLite database: {e}")
    return None

# Create tables
def create_tables():
    conn = create_connection()
    if conn:
        try:
            create_users_table = """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                chat_id INTEGER NOT NULL UNIQUE,
                username TEXT,
                date_of_join TEXT,
                subscription_level TEXT DEFAULT 'free',
                daily_quota INTEGER DEFAULT 5,
                referral_code TEXT,
                images_processed_today INTEGER DEFAULT 0,
                total_images_processed INTEGER DEFAULT 0,
                last_reset TEXT,
                referrals INTEGER DEFAULT 0,
                referrer INTEGER DEFAULT NULL
            );
            """
            create_stats_table = """
            CREATE TABLE IF NOT EXISTS stats (
                id INTEGER PRIMARY KEY,
                total_users INTEGER DEFAULT 0,
                total_images_processed INTEGER DEFAULT 0
            );
            """
            conn.execute(create_users_table)
            conn.execute(create_stats_table)
            conn.commit()
        except Exception as e:
            logger.error(f"Error creating tables: {e}")
        finally:
            conn.close()

create_tables()

# Initialize stats table
def initialize_stats():
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM stats")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO stats (total_users, total_images_processed) VALUES (0, 0)")
            conn.commit()
        conn.close()

initialize_stats()

# Generate a 10-digit referral code
def generate_referral_code():
    return ''.join(random.choices(string.digits, k=10))

# Check or create user entry
async def check_or_create_user(user_id, username, context, referrer_id=None):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE chat_id = ?", (user_id,))
        row = cursor.fetchone()
        if row is None:
            date_of_join = str(datetime.datetime.now())
            referral_code = generate_referral_code()
            cursor.execute(
                "INSERT INTO users (chat_id, username, date_of_join, referral_code, last_reset, referrer) VALUES (?, ?, ?, ?, ?, ?)",
                (user_id, username, date_of_join, referral_code, date_of_join, referrer_id)
            )
            cursor.execute("UPDATE stats SET total_users = total_users + 1")
            if referrer_id:
                cursor.execute("UPDATE users SET daily_quota = daily_quota + 2, referrals = referrals + 1 WHERE chat_id = ?", (referrer_id,))
                cursor.execute("UPDATE users SET daily_quota = daily_quota + 2 WHERE chat_id = ?", (user_id,))
                conn.commit()
                cursor.execute("SELECT daily_quota FROM users WHERE chat_id = ?", (referrer_id,))
                new_quota = cursor.fetchone()[0]
                cursor.execute("SELECT username FROM users WHERE chat_id = ?", (referrer_id,))
                referrer_username = cursor.fetchone()[0]
                referrer_info_message = f"✅ You have successfully invited {username} using a referral link! Your daily quota has been increased by 2 images."
                await context.bot.send_message(chat_id=referrer_id, text=referrer_info_message)
                user_message = f"✅ You have successfully used a referral link! Your daily quota has been increased by 2 images. Invited by {referrer_username}"
                await context.bot.send_message(chat_id=user_id, text=user_message)
        conn.commit()
        conn.close()

# Get user by referral code
def get_user_by_referral_code(referral_code):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE referral_code = ?", (referral_code,))
        user = cursor.fetchone()
        conn.close()
        return user
    return None

# Reset the daily quota at midnight
async def reset_daily_quotas(context: CallbackContext) -> None:
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT chat_id, subscription_level FROM users")
        users = cursor.fetchall()
        for user in users:
            chat_id, subscription_level = user
            if subscription_level == 'free':
                cursor.execute(
                    "UPDATE users SET images_processed_today = 0, daily_quota = 5, last_reset = ? WHERE chat_id = ?",
                    (str(datetime.datetime.now()), chat_id)
                )
            elif subscription_level == 'premium':
                cursor.execute(
                    "UPDATE users SET images_processed_today = 0, daily_quota = -1, last_reset = ? WHERE chat_id = ?",
                    (str(datetime.datetime.now()), chat_id)
                )
        conn.commit()
        conn.close()

# Command to start the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    username = update.message.from_user.username

    if update.message.text.startswith('/start '):
        ref_code = update.message.text.split(' ')[1]
        ref_user = get_user_by_referral_code(ref_code)
        if ref_user:
            if ref_user[1] == user_id or ref_user[10] == user_id:
                await update.message.reply_text('❌ You cannot use your own referral link.')
                return
            elif ref_user:
                await check_or_create_user(user_id, username, context, ref_user[1])
                return
        else:
            await check_or_create_user(user_id, username, context)
            referral_link = f"https://t.me/yt_dlbot?start={ref_code}"
            await update.message.reply_text(f'👋 Welcome! Send me an image and I will remove the background for you. Use /help for more info.\nYour referral link: {referral_link}')
            return
    await check_or_create_user(user_id, username, context)

    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT referral_code FROM users WHERE chat_id = ?", (user_id,))
    referral_code = cursor.fetchone()[0]
    conn.close()

    referral_link = f"https://t.me/{BOT_USERNAME}?start={referral_code}"
    await update.message.reply_text(f'👋 Welcome! Send me an image and I will remove the background for you. Use /help for more info.\nYour referral link: {referral_link}')

# Command to display help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Send me an image, and I will remove the background for you. You can also use inline commands!')

# Command to display usage
async def usage_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT subscription_level, daily_quota, images_processed_today, total_images_processed, referral_code FROM users WHERE chat_id = ?", (user_id,))
    user_data = cursor.fetchone()
    conn.close()

    remaining_quota = "Unlimited" if user_data[1] == -1 else user_data[1] - user_data[2]
    referral_link = f"https://t.me/{BOT_USERNAME}?start={user_data[4]}"
    await update.message.reply_text(
        f'📊 Usage Info:\n'
        f'Subscription Level: {user_data[0]}\n'
        f'Allowed Daily Quota: {user_data[1] if user_data[1] != -1 else "Unlimited"}\n'
        f'Used Quota: {user_data[2]}\n'
        f'Remaining Quota: {remaining_quota}\n'
        f'Total Images Processed: {user_data[3]}\n'
        f'Your Referral Link: {referral_link}'
    )

# Command to display referral info
async def referral_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT referrals, referral_code FROM users WHERE chat_id = ?", (user_id,))
    user_data = cursor.fetchone()
    conn.close()

    referral_link = f"https://t.me/{BOT_USERNAME}?start={user_data[1]}"
    await update.message.reply_text(
        f'📊 Referral Info:\n'
        f'Daily Quota Added Per Referral: 2\n'
        f'Users Invited: {user_data[0]}\n'
        f'Your Referral Link: {referral_link}'
    )

# Function to handle image processing
async def image_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT subscription_level, images_processed_today, daily_quota FROM users WHERE chat_id = ?", (user_id,))
    user_data = cursor.fetchone()
    referral_link = f"https://t.me/{BOT_USERNAME}?start={user_data[1]}"
    if user_data[1] >= user_data[2] and user_data[2] != -1:
        await update.message.reply_text(
            f'❌ You have reached your daily quota. Try again tommorow or invite more users to increase your daily quota. \n'
            f'Your Referral Link: {referral_link}'            
        )
        return

    progress_message = await update.message.reply_text("Processing your image, please wait...")

    try:
        file = await update.message.photo[-1].get_file()
        async with httpx.AsyncClient(timeout=httpx.Timeout(60.0)) as client:
            response = await client.get(file.file_path)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content))
            output = remove(np.array(img))
            img = Image.fromarray(output).convert("RGBA")

            with BytesIO() as image_binary:
                img.save(image_binary, 'PNG')
                image_binary.seek(0)
                await update.message.reply_document(document=InputFile(image_binary, 'no_bg.png'))

        cursor.execute(
            "UPDATE users SET images_processed_today = images_processed_today + 1, total_images_processed = total_images_processed + 1 WHERE chat_id = ?",
            (user_id,)
        )
        cursor.execute("UPDATE stats SET total_images_processed = total_images_processed + 1")
        conn.commit()

        remaining_quota = "Unlimited" if user_data[2] == -1 else user_data[2] - user_data[1] - 1
        await update.message.reply_text(f"✅ Here is your image with the background removed!\nRemaining Daily Quota: {remaining_quota}")

    except Exception as e:
        logger.error(f"Error processing image: {e}")
        await update.message.reply_text("❌ An error occurred while processing your image. Please try again later.")
    
    finally:
        await progress_message.delete()
        conn.close()

# Function to handle inline queries
async def inline_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.inline_query.query
    if not query:
        return

    result = InlineQueryResultPhoto(
        id=query.upper(),
        title="Send me an image",
        photo_url="https://example.com/default_image.png",
        thumb_url="https://example.com/default_image.png"
    )
    await update.inline_query.answer([result])

# Command to display statistics
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT total_users, total_images_processed FROM stats")
    stats_data = cursor.fetchone()
    conn.close()

    stats_message = (
        f"📊 Statistics:\n\n"
        f"Total Users: {stats_data[0]}\n"
        f"Total Images Processed: {stats_data[1]}"
    )
    
    await context.bot.send_message(
        chat_id=CHANNEL_PRIVATE_LINK,
        text=stats_message
    )

def main() -> None:
    # Create the application
    application = Application.builder().token(BOT_TOKEN).build()

    # Handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('usage', usage_command))
    application.add_handler(CommandHandler('referral', referral_command))
    application.add_handler(CommandHandler('stats', stats))
    application.add_handler(MessageHandler(filters.PHOTO, image_handler))
    application.add_handler(InlineQueryHandler(inline_query_handler))

    # Set up the job queue
    job_queue = application.job_queue
    job_queue.run_daily(reset_daily_quotas, datetime.time(hour=0, minute=0, second=0))

    # Run the bot
    application.run_polling()

if __name__ == '__main__':
    main()
