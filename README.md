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

## Files
* Procfile
* timeline_api.py
* user_api.py
* README.md
* haproxy-config
  * Configuration file for HAProxy
* bin/init.sh
  * Script for creating the project's databases
* share/following.csv
* share/posts.csv
* share/users.csv
* var/
  * An empty directory that will hold our databases
  
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


### Poll Service

### Service Registry Service

* POST /register/
  * Takes a service's address and adds it to the registry
