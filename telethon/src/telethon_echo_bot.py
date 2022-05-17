from telethon import TelegramClient, events
from conf.settings import TELEGRAM_TOKEN as TOKEN
from conf.settings import API_ID, API_HASH, PHONE


client = TelegramClient(PHONE, API_ID, API_HASH)

bot = client.start(bot_token=TOKEN)

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    """Send a message when the command /start is issued."""
    await event.respond('Hi!')
    raise events.StopPropagation

@bot.on(events.NewMessage)
async def echo(event):
    """Echo the user message."""
    await event.respond(event.text)

def main():
    """Start the bot."""
    bot.run_until_disconnected()

if __name__ == '__main__':
    main()