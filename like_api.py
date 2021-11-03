import hug
import redis
import requests


r = redis.Redis()
redisKey = 0
r.flushall()


# TODO APIs
'''
@hug.get("/likes/{username}")
def retrieve_user_likes(response, id: hug.types.number):
    """GET a list of posts that a user liked"""
    likes = []
    try:
        post = db["posts"].get(id)
        posts.append(post)
    except sqlite_utils.db.NotFoundError:
        response.status = hug.falcon.HTTP_404
    return {"likes": likes}

@hug.get("/likes/{id}")
def retrieve_post_likes(response, id: hug.types.number):
    """GET the number of likes a post has"""
    likes = []
    try:
        post = db["posts"].get(id)
        posts.append(post)
    except sqlite_utils.db.NotFoundError:
        response.status = hug.falcon.HTTP_404
    return {"likes": likes}
'''


@hug.post("/likes/", status=hug.falcon.HTTP_201)
def like_post(
    username: hug.types.text,
    post: hug.types.number,
    response,
):
    """POST a new like"""
    global redisKey

    like = {
        "username": username,
        "post_id": post,
    }

    try:
        r.hmset(redisKey, like)
        redisKey += 1
    except Exception as e:
        response.status = hug.falcon.HTTP_409
        return {"error": str(e)}

    return like
