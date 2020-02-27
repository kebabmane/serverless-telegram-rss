from __future__ import print_function
import json
import telegram
import os
import logging

# Logging is cool!
logger = logging.getLogger()
if logger.handlers:
    for handler in logger.handlers:
        logger.removeHandler(handler)
logging.basicConfig(level=logging.INFO)

def configure_telegram():
    """
    Configures the bot with a Telegram Token.
    Returns a bot instance.
    """

    TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
    if not TELEGRAM_TOKEN:
        logger.error('The TELEGRAM_TOKEN must be set')
        raise NotImplementedError

    return telegram.Bot(TELEGRAM_TOKEN)

def lambda_handler(event, context):
    bot = configure_telegram()
    for record in event['Records']:
        bot.send_message(record)
    print('Successfully processed %s records.' % str(len(event['Records'])))
