from __future__ import print_function
import json
import os
import logging
import boto3
import feedparser
from boto3.dynamodb.conditions import Key, Attr

# Logging is cool!
logger = logging.getLogger()
if logger.handlers:
    for handler in logger.handlers:
        logger.removeHandler(handler)
logging.basicConfig(level=logging.INFO)

# Bring in the OS Vars from Lambda Runtime
# queue_url = os.environ['LAMBDA_QUEUE']
dynamodb_feeds_table_name = os.environ['FEEDS_DYNAMODB_TABLE']
dynamodb_entries_table_name = os.environ['DYNAMODB_TABLE']

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    feeds_table = dynamodb.Table(dynamodb_feeds_table_name)
    entries_table = dynamodb.Table(dynamodb_entries_table_name)

    response = feeds_table.scan()
    for item in response['Items']:
        rss_link = item['id']
        print(rss_link)
        d = feedparser.parse(rss_link)
        for entry in d.entries:
            print(entry.link)
            entries_response = entries_table.get_item(
                    Key={'id': entry.link}
             )
            item = entries_response.get('Item')
            if item:
                 print(item)
            else:
                entries_table.put_item(
                       Item={'id': entry.link}
                )