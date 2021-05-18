import datetime
import json
import logging
import os
import urllib.parse
import boto3
import pandas as pd
from botocore.exceptions import ClientError

# set env var
sqs_queue_url = os.getenv("SQS_QUEUE_URL")
dynamo_table = os.getenv("TABLE_NAME")

# get boto client
sqs_client = boto3.client("sqs")
s3_client = boto3.client("s3")

# client = boto3.client("sns", region_name="eu-west-1",
#                       aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)


def lambda_handler(event, context):
    print("receievd event as:", json.dumps(event))
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = urllib.parse.unquote_plus(
        event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        obj = s3_client.get_object(Bucket=bucket, Key=key)
        print("CONTENT TYPE: " + obj['ContentType'])  # parse csv file
        if obj["ContentType"] == "text/csv":
            csv_obj = pd.read_csv(obj["Body"])
            for _, row in csv_obj.iterrows():
                msg = convert_row(row)
                send_sqs_msg(msg)

    except Exception as e:
        print(e)
        print(f"Error getting object {key} from bucket {bucket}")
        raise e


def convert_row(row):
    """
    Convert CSV file row to a dicitonary object that fits into Dynamodb table later. 
    The object is then converted into json to prepare itself sent through SQS msg. 
    """
    converted_ts = datetime.datetime.fromtimestamp(float(row['timestamp']))
    message = {
        "TableName": dynamo_table,
        "Item": {
            "date": {
                "S": str(converted_ts.date())
            },
            "time":
            {
                "S": str(converted_ts.time().strftime('%H:%M:%S'))
            },
            "location":
            {
                "S": row["location"]
            },
            'source':
            {
                'S': row['source']
            },
            'local_dest':
            {
                'S': row['local_dest']
            },
            'local_avg':
            {
                'N': row['local_avg']
            },
            'remote_dest':
            {
                'S': row['remote_dest']
            },
            'remote_avg':
            {
                'N': row['remote_avg']
            }
        }
    }
    json_msg = json.dumps(message)
    return json_msg


def send_sqs_msg(msg):
    """
    Send Json messge to SQS
    :param msg: String
    :return: Dictionary containing information about the sent message. If
        error, returns None.
    """
    try:
        msg = sqs_client.send_message(
            QueueUrl=sqs_queue_url,
            MessageBody=msg,
            MessageAttributes={
                "Method": {
                    "StringValue": "POST",
                    "DataType": "String"
                }
            }
        )
    except ClientError as e:
        print("Failed to send csv row to sqs", e)
        return None
    print("SQS MESSAGE RESPONSE\n", msg)
    return msg
