from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import logging
import os

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define your command handlers
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi! Send me a text to search in the book content.')

def search(update: Update, context: CallbackContext) -> None:
    user_text = update.message.text
    results = search_books(user_text)
    update.message.reply_text(results)

def search_books(query: str) -> str:
    with open('/books.txt', 'r') as file:
        content = file.read()
        lines = content.split('\n')
        results = [line for line in lines if query.lower() in line.lower()]
        if results:
            return '\n'.join(results[:5])  # Return top 5 results
        else:
            return "No results found."

def main() -> None:
    # Get the token from environment variables
    token = os.getenv("TELEGRAM_TOKEN")
    updater = Updater(token, use_context=True)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, search))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
