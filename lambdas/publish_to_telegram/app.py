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

def extract_values(obj, key):
    """Pull all values of specified key from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    results = extract(obj, arr, key)
    return results

def lambda_handler(event, context):
    TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
    bot = configure_telegram()
    for record in event['Records']:
        d = json.loads(record['body'])
        print(d['dynamodb']['Keys']['id']['S'])
        bot.send_message(text=d['dynamodb']['Keys']['id']['S'], chat_id=TELEGRAM_CHAT_ID)
    print('Successfully processed %s records.' % str(len(event['Records'])))
    return
