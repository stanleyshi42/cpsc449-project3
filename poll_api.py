import hug
import boto3
import requests
import os


poll_id = 0
dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")


@hug.get("/health-check/")
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
                "attributes": {"Question:": question}
            }
        )
        table.put_item(
            Item={
                "p_key": "POL#" + str(poll_id),
                "s_key": "OPT#" + str(poll_id),
                "attributes": attributes
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


# TODO get a poll
@hug.get("/polls/{poll_id}", status=hug.falcon.HTTP_201)
def retrieve_poll(poll_id: hug.types.number, response):
    table = dynamodb.Table("Polls")
    poll_id = "POL#" + str(poll_id)
    opt_id = "OPT#" + str(poll_id)

    poll = {}

    #TODO
    try:
        response = table.get_item(Key={"p_key": poll_id, "s_key": poll_id})
        # response = table.get_item(Key={"p_key": poll_id, "s_key": opt_id})
    except Exception as e:
        return {"error": str(e.response["Error"]["Message"])}
    print(response)
    return response["Item"]

@hug.startup()
@hug.post(status=hug.falcon.HTTP_201)
def register(url: hug.types.text):
    """Register with the Service Registry"""
    port = os.environ.get("PORT")
    url = 'http://localhost:'+port
    requests.post("http://localhost:4400/register/",data={'url':url})
    print('done')