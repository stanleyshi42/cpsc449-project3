import hug
import boto3
from boto3.dynamodb.conditions import Key


poll_id = 0
dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")


def create_poll_table():
    # dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")
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


def put_poll(p_key, s_key, attributes):
    # dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")
    table = dynamodb.Table("Polls")
    print("Adding to table:", attributes)
    try:
        response = table.put_item(
            Item={
                "p_key": p_key,
                "s_key": s_key,
                "attributes": attributes,
            }
        )
    except Exception as e:
        # response.status = hug.falcon.HTTP_409
        print("ERROR: ", str(e))
        return {"error": str(e)}

    return response


@hug.get("/health/")
def health():
    return {"health": "alive"}


@hug.post(
    "/polls/",
    status=hug.falcon.HTTP_201,
)
def create_poll(
    question: hug.types.text,
    opt1: hug.types.text,
    opt2: hug.types.text,
    response,
    opt3: hug.types.text = None,
    opt4: hug.types.text = None,
):
    """POST a new poll; minimum 2 poll options"""
    global poll_id
    # dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")
    table = dynamodb.Table("Polls")

    attributes = {}
    attributes["Option1"] = opt1
    attributes["Option2"] = opt2
    if opt3:
        attributes["Option3"] = opt3
    if opt4:
        attributes["Option4"] = opt4

    try:
        table.put_item(
            Item={
                "p_key": "POL#" + str(poll_id),
                "s_key": "POL#" + str(poll_id),
                "attributes": {"Question:": question},
            }
        )
        poll = table.put_item(
            Item={
                "p_key": "POL#" + str(poll_id),
                "s_key": "OPT#" + str(poll_id),
                "attributes": attributes,
            }
        )
        poll_id += 1
    except Exception as e:
        response.status = hug.falcon.HTTP_409
        return {"error": str(e)}

    attributes["Question"] = question
    return {
        "p_key": "POL#" + str(poll_id),
        "s_key": "POL#" + str(poll_id),
        "attributes": attributes,
    }


# TODO
@hug.get("/polls/{poll_id}", status=hug.falcon.HTTP_201)
def retrieve_poll(poll_id: hug.types.number, response):
    table = dynamodb.Table("Polls")
    poll_id = "POL#" + str(poll_id)
    opt_id = "OPT#" + str(poll_id)

    poll = {}

    try:
        response = table.get_item(Key={"p_key": poll_id, "s_key": poll_id})
        # response = table.get_item(Key={"p_key": poll_id, "s_key": opt_id})
    except Exception as e:
        return {"error": str(e.response["Error"]["Message"])}
    print(response)
    return response["Item"]


if __name__ == "__main__":
    table = create_poll_table()
    print("Table status:", table.table_status)

    put_poll("POL#1", "POL#1", {"Question": "What's your favorite day?"})
    attributes = {}
    attributes["Option1"] = "Friday"
    attributes["Option2"] = "Saturday"
    attributes["Option3"] = "Sunday"
    attributes["Option4"] = "Monday"

    put_poll(
        "POL#1",
        "OPT#1",
        attributes,
    )

    """
    # Query
    dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")
    table = dynamodb.Table("Polls")
    
    query = table.query(KeyConditionExpression=Key("p_key").eq("POL#1"))
    query = query["Items"]
    
    for item in query:
        print(item["p_key"], " :", item["attributes"])
    print(query)
    print(query[0]["attributes"])
    """
