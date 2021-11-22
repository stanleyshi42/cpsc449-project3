# CPSC 449 Project 3

## Team Members
- Stanley Shi

## Database Setup
To start DynamoDB, navigate to the project directory and use:
```bash
cd DynamoDB/
java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb
```
Keep this terminal open until you are done using the project.

To create each databse, start a new terminal in the project directory and use:
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
### User Service (Port 4000)
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
  
### Timeline Service (Port 4100)
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

### Like Service (Port 4200)
* GET /users/{username}/likes/
  * Returns posts a user has liked
* GET /posts/{post_id}/likes/
  * Returns number of likes a post has
* POST /posts/{post_id}/likes/
  * Posts a new like to a post
  * http post localhost:4200/posts/0/likes username=stan98
* GET /posts/popular/
  * Returns popular posts

### Poll Service (Port 4300)
* POST /polls/
  * Creates a new poll; allows between 2 and 4 options
  * http post localhost:4300/polls/ question='Favorite color?' opt1=red opt2=green opt3=blue opt4=white
* GET /polls/{poll_id}
  * Returns a poll

### Service Registry Service (Port 4400)
* POST /register/
  * Takes a service's address and adds it to the registry
  
## Shortcomings
* GET popular posts not implemented
* Voting on polls not implemented
* GET poll not fully implemented
* Project breaks if multiple instances of services are made
