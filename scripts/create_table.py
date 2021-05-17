import boto3

dynamodb = boto3.resource('dynamodb')
table_name = "TableViper"


def main():
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                "AttributeName": "timestamp",
                "KeyType": "HASH"  # partition key
            },
            {
                "AttributeName": "location",
                "KeyType": "RANGE"  # sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'timestamp',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'location',
                'AttributeType': 'S'
            },
        ],
    )

    # Wait until the table exists.
    table.meta.client.get_waiter("table_exists").wait(TableName=table_name)

    # Print out some data about the table.
    print(table.item_count)


if __name__ == '__main__':
    main()
