## A Chatting app API implemented using FastAPI.

## Features:
- Signin: Authenticating users using oauth2
- Signup
- `/chat/ws`: This endpoint starts a websocket connection with `wss://echo.websocket.org`, and all messages are saved in a MongoDB.


## Folders structure:
- `/api`: Contains all endpoints routing functions (router).
- `/core`: Contains core functionalities to the server. (middlewares(Dependencies) and configurations from .env file).
- `/models`: Contains database object models
- `/schemas`: Contains the request and response to endpoints data structure. (Like a DTO in Java)
- `/services`: Contains services that affect database, so they can be in one place and easily reused


## How to run:
- Run `pip install -r requirements.txt`
- Run server: `uvicorn main:app --reload`

- Frontend using React(Typescript): https://github.com/MohamedRostom0/ChatApp-React
