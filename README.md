# CPSC 449 Project 3

## Team Members
- Stanley Shi

## Database Setup
In the project directory, use:
```bash
./bin/init.sh
python3 bin/init_dynamodb.py 
```

## Running the Project
In the project directory, use:
```bash
foreman start
```

Now, HTTP requests can be made to the project's services.

## Health Check
Each service has an endpoint called /health-check/ that returns 200.
The service registry service periodically performs a health check with each service by making a request to that endpoint.
  
## API Endpoints
### Timeline Service
* GET /public_timeline/
  * Returns Public Timeline
* GET /user_timeline/{username}
  * Returns the User Timeline of a specific user
* GET /home_timeline/
  * Requires user auth
  * Returns the Home Timeline of a specific, authenticated user
* GET /posts/{id}
  * Return a specific post by ID
* POST /posts/
  * Requires user auth
  * Creates a post

### User Service
* GET /users/
  * Returns all users
* GET /users/{username}
  * Returns a specific user by username
* POST /users/
  * Creates a new user
* GET /users/{username}/following/
  * Gets a user's following list
* POST /users/{username}/following/
  * Adds a new user to a specific user's following list

### Like Service
* GET /users/{username}/likes/
  * Returns posts a user has liked
* GET /posts/{post_id}/likes/
  * Returns number of likes a post has
* POST /posts/{post_id}/likes/
  * Posts a new like to a post
* GET /posts/popular/
  * Returns popular posts

### Poll Service
* POST /polls/
  * Creates a new poll; allows between 2 and 4 options
  * http post localhost:4300/polls/ question='Favorite color?' opt1=red opt2=green opt3=blue opt4=white
* GET /polls/{poll_id}
  * Returns a poll

### Service Registry Service
* POST /register/
  * Takes a service's address and adds it to the registry
  
## Shortcomings
* GET popular posts not implemented
* Voting on polls not implemented
* GET poll not fully implemented
* Project breaks if multiple instances of services are made
