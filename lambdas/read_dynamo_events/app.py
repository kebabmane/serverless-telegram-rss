from __future__ import print_function
import json
import os
import logging
import boto3
from botocore.exceptions import ClientError

# Logging is cool!
logger = logging.getLogger()
if logger.handlers:
    for handler in logger.handlers:
        logger.removeHandler(handler)
logging.basicConfig(level=logging.INFO)

# Bring in the OS Vars from Lambda Runtime
# queue_url = os.environ['LAMBDA_QUEUE']
queue_name = os.environ['LAMBDA_QUEUE']

def send_sqs_message(QueueName, msg_body):
    """

    :param sqs_queue_url: String URL of existing SQS queue
    :param msg_body: String message body
    :return: Dictionary containing information about the sent message. If
        error, returns None.
    """

    # Send the SQS message
    sqs_client = boto3.client('sqs')    
    sqs_queue_url = sqs_client.get_queue_url(QueueName=QueueName)['QueueUrl'] 
    try:
        msg = sqs_client.send_message(QueueUrl=sqs_queue_url,
                                      MessageBody=json.dumps(msg_body)) 
    except ClientError as e:
        logging.error(e) 
        return None
    return msg

def lambda_handler(event, context):
    for record in event['Records']:
            # Send some SQS messages
            msg = send_sqs_message(queue_name,record)
            if msg is not None:
                logging.info(f'Sent SQS message ID: {msg["MessageId"]}')
            return {
                'statusCode': 200,
                'body': json.dumps(record)
            }
    print('Successfully processed %s records.' % str(len(event['Records'])))
    return
