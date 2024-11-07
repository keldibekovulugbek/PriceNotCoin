import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackContext, JobQueue

# Replace with your actual bot token
TELEGRAM_BOT_TOKEN = 'Your bot token'

# Dictionary to store the last known price of NOT coin
last_prices = {
    'notcoin': None
}

# Set of chat IDs to notify
chat_ids = set()

# Function to get the current price of a cryptocurrency from CoinGecko
def get_crypto_price(crypto_id: str):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    return data[crypto_id]['usd']

# Function to handle the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    chat_ids.add(chat_id)
    await update.message.reply_text("Ulug'bekning botiga xush kelibsiz! Bu bot notkoin narxi o'zgarsa xabar beradi.")

# Function to send the crypto price whenever it changes
async def send_crypto_price(context: CallbackContext):
    global last_prices
    notcoin_price = get_crypto_price('notcoin')

    price_message = f"NOT narxi: ${notcoin_price}"

    # Check NOT coin price change
    if last_prices['notcoin'] is None or notcoin_price != last_prices['notcoin']:
        last_prices['notcoin'] = notcoin_price
        # Send message to all users who have started the bot
        for chat_id in chat_ids:
            await context.bot.send_message(chat_id=chat_id, text=price_message)

# Function to handle the /track command to start tracking crypto prices
async def track(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.job_queue.run_repeating(send_crypto_price, interval=60, first=0)
    await update.message.reply_text('Kuzatish boshlandi!')

def main():
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Initialize JobQueue
    job_queue = application.job_queue

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("track", track))

    # Run the bot
    application.run_polling()

if __name__ == '__main__':
    main()
