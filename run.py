import os
from app import create_app,  socketio
from os import environ
from dotenv import load_dotenv


env = environ.get("FLASK_ENV", "development")

load_dotenv()
app= create_app()



if __name__ == "__main__":
     
    if env == "development":
        socketio.run(app,host="0.0.0.0",port=4000,debug=True)
    else:
        socketio.run(app, host="0.0.0.0", port=4000)
