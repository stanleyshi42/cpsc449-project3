import hug
import boto3
from boto3.dynamodb.conditions import Key

def delete_table(table):
    table.delete()


def create_poll_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")

    delete_table(dynamodb.Table("Polls"))  # TODO delete this line
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


def put_poll(p_key, s_key, attributes={}, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")

    table = dynamodb.Table("Polls")
    response = table.put_item(
        Item={
            "p_key": p_key,
            "s_key": s_key,
            "attributes": attributes,
        }
    )
    
    return response


if __name__ == "__main__":
    movie_table = create_poll_table()
    print("Table status:", movie_table.table_status)
    put_poll("POL#1", "POL#1", {"Question": "Favorite color?"})
    put_poll(
        "POL#1",
        "OPT#1",
        {"Option1": "Red", "Option2": "Green", "Option3": "Blue", "Option4": "White"},
    )
    dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")
    table = dynamodb.Table("Polls")
    query = table.query(
        KeyConditionExpression=Key('p_key').eq("POL#1")
    )
    query = query['Items']
    for item in query:
        print(item['p_key'], ' :',item['attributes'])
    print(query)
    print(query[0]['attributes'])
    