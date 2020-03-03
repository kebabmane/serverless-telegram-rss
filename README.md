# RSS to Telgram Bot

Couldn't find it so I decided to make it!

I wanted an easy way to watch an RSS feed and pump the output through to a telegram bot/channel for consumption throughout the day, I couldn't find one that fit nicely into AWS Serverless so I built this;

Logcically;
- A RSS Entires DynamoDB table has a basic schema of ID: feed_url
- parse_feeds_to_dynamodb runs every 5 minutes (cloudwatch cron), iterates over the entries in the Entires Table and posts the links found in any RSS feed entries to the Dynamo Events Table
- the dynamodb events table has a stream (NEW_AND_OLD_IMAGES) that triggers another lambda, this lambda strips the message down and forwards onto an SQS Queue (not really required but I was focused on guaranteed delivery of items)

Simply this Serverless stack creates;

- Two DynamoDB Tables (one with a stream)
- an SQS Queue
- IAM Roles
- 3x Lambdas