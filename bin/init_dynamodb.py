import boto3


def create_poll_table():
    dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")
    if dynamodb.Table("Polls"):
        dynamodb.Table("Polls").delete()

    table = dynamodb.create_table(
        TableName="Polls",
        KeySchema=[
            {"AttributeName": "p_key", "KeyType": "HASH"},  # Partition key
            {"AttributeName": "s_key", "KeyType": "RANGE"},  # Sort key
        ],
        AttributeDefinitions=[
            {"AttributeName": "p_key", "AttributeType": "S"},
            {"AttributeName": "s_key", "AttributeType": "S"},
        ],
        ProvisionedThroughput={"ReadCapacityUnits": 10, "WriteCapacityUnits": 10},
    )
    return table


if __name__ == "__main__":
    table = create_poll_table()
    print("Table status:", table.table_status)
