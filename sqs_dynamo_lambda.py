import logging
import json
import boto3

# get boto client
dynamo_client = boto3.client('dynamodb')

# cold start
operations = {
    "POST": lambda dynamo, x: dynamo.put_item(**x),
    "PUT": lambda dynamo, x: dynamo.update_item(**x),
    'GET': lambda dynamo, x: dynamo.get_item(**x),
    'GET_ALL': lambda dynamo, x: dynamo.scan(**x),
    'DELETE': lambda dynamo, x: dynamo.delete_item(**x),
    'BATCH_WRITE': lambda dynamo, x: dynamo.batch_write_item(**x),
}


def lambda_handler(event, context):
    print("CONTEXT", context)
    for record in event["Records"]:
        payload = json.loads(record["body"], parse_float=str)
        #  payload is the same as the message dictionary in convert_row() in s3_sqs_lambda
        print("PAYLOAD", payload)
        # note the capitalLetters
        operation = record["messageAttributes"]["Method"]["stringValue"]
        if operation in operations:
            try:
                operations[operation](dynamo_client, payload)
            except Exception as e:
                # return -1
                raise e
        else:
            print(f"Unsupported method \'{operation}\' ")
            raise Exception(f"Unsupported method \'{operation}\' ")
    return  # return 0
