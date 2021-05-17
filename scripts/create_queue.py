import boto3

sqs = boto3.client("sqs")
queue_name = "QueueViper"


def main():
    response = sqs.create_queue(
        QueueName=queue_name,
    )
    print("Create", response["QueueUrl"])


if __name__ == "__main__":
    main()
