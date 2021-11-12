import hug
import redis


r = redis.Redis()
redisKey = 0
r.flushall()


# Insert sample data into Redis
r.hmset(redisKey, {"username": "jack_jackson", "post_id": 0})
redisKey += 1
r.hmset(redisKey, {"username": "john_johnson", "post_id": 3})
redisKey += 1
r.hmset(redisKey, {"username": "jack_jackson", "post_id": 2})
redisKey += 1
r.hmset(redisKey, {"username": "stan98", "post_id": 0})
redisKey += 1
r.hmset(redisKey, {"username": "stan98", "post_id": 1})
redisKey += 1


@hug.get("/health/")
def health():
    return {"health": "alive"}

@hug.get("/users/{username}/likes/")
def retrieve_user_likes(response, username: hug.types.text):
    """GET a list of posts that a user has liked"""
    posts = []

    try:
        # Iterate through all hashes
        for i in range(redisKey):
            likes = r.hgetall(i)
            # Decode dict of bytes to strings
            likes = {key.decode(): value.decode() for key, value in likes.items()}
            if likes["username"] == username:
                posts.append(likes["post_id"])
    except Exception as e:
        response.status = hug.falcon.HTTP_409
        return {"error": str(e)}

    return {"liked_posts": posts}


@hug.get("/posts/{post_id}/likes/")
def retrieve_post_likes(response, post_id: hug.types.number):
    """GET the number of likes a post has"""
    like_count = 0

    try:
        # Iterate through all hashes
        for i in range(redisKey):
            likes = r.hgetall(i)
            # Decode dict of bytes to strings
            likes = {key.decode(): value.decode() for key, value in likes.items()}
            if int(likes["post_id"]) == post_id:
                like_count += 1
    except Exception as e:
        response.status = hug.falcon.HTTP_409
        return {"error": str(e)}

    return {"post_id": post_id, "likes": like_count}


@hug.post("/posts/{post_id}/likes/", status=hug.falcon.HTTP_201)
def like_post(
    username: hug.types.text,
    post_id: hug.types.number,
    response
):
    """POST a new like"""
    global redisKey

    like = {
        "username": username,
        "post_id": post_id,
    }

    try:
        r.hmset(redisKey, like)
        redisKey += 1
    except Exception as e:
        response.status = hug.falcon.HTTP_409
        return {"error": str(e)}

    return like

#TODO API to GET popular posts