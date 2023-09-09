import os
import requests
import logging
import random
import time

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, Job

ChannelID = "-1001973476872"
ChannelLink = "@mtproxyfinder"

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Flag to track whether the proxy has been sent
proxy_sent = False

# get random line from url
def get_random_line_from_url(url):
    response = requests.get(url)
    lines = response.text.splitlines()
    return random.choice(lines) if lines else None

# send proxy only once
async def send_proxy(context: ContextTypes.DEFAULT_TYPE) -> None:
    global proxy_sent
    if proxy_sent:
        return

    url = "https://github.com/mtproxyfinder/proxylist/raw/main/list.txt"
    CH_ID = "-1001973476872"
    ADMIN_ID = "1301600392"
    proxy = get_random_line_from_url(url)
    # parse proxy
    parsed_server = proxy.split("=")[1].split("&")[0]
    parsed_port = proxy.split("=")[2].split("&")[0]
    parsed_secret = proxy.split("=")[3]
    # create message
    text = f"""
    پروکسی تست شده
server: {parsed_server}
port: {parsed_port}
secret: {parsed_secret}
{ChannelLink}
    """
    # add proxy as button to message
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="Connect-اتصال", url=proxy)
            ],
            [
                InlineKeyboardButton(text="Emergency Connect-اتصال اورژانسی", url="https://mtproxyfinder.github.io"),
            ]
        ]
    )

    if proxy:
        # Send proxy to channel
        print("sending proxy")
        await context.bot.send_message(chat_id=CH_ID, text=text, reply_markup=reply_markup)
        proxy_sent = True
    else:
        # send error to admin
        print("sending error to admin")
        await context.bot.send_message(chat_id=ADMIN_ID, text="Error: no proxy found")

def main() -> None:
    BotToken = os.environ.get("TOKEN")
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(BotToken).build()
    
    # Add send proxy job to application
    application.job_queue.run_once(send_proxy, name="send_proxy", when=1)
    
    # Run the bot until the user presses Ctrl-C or proxy_sent becomes True
    while not proxy_sent:
        try:
            application.run_polling(allowed_updates=Update.ALL_TYPES)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
