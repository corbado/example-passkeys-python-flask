from flask import Flask, render_template, request, jsonify
from werkzeug.exceptions import Unauthorized
from jose import jwt
from dotenv import load_dotenv
import os
import requests

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

PROJECT_ID = os.environ.get("PROJECT_ID")
API_SECRET = os.environ.get("API_SECRET")

# Session config
short_session_cookie_name = "cbo_short_session"
issuer = f"https://{PROJECT_ID}.frontendapi.corbado.io"
jwks_uri = f"https://{PROJECT_ID}.frontendapi.corbado.io/.well-known/jwks"


class User:
    def __init__(self, is_valid, sub=None, name=None, email=None):
        self.is_valid = is_valid
        self.sub = sub
        self.name = name
        self.email = email


class Session:
    def __init__(self, app, short_session_cookie_name, issuer, jwks_uri):
        self.app = app
        self.short_session_cookie_name = short_session_cookie_name
        self.issuer = issuer
        self.jwks_uri = jwks_uri

    def get_current_user(self):
        token = request.cookies.get(self.short_session_cookie_name)

        if not token:
            return User(False)

        try:
            jwks = requests.get(self.jwks_uri).json()
            public_key = jwks["keys"][0]

            payload = jwt.decode(
                token,
                key=public_key,
                algorithms=["RS256"],
                audience=self.app.config.get("API_SECRET"),
                issuer=self.issuer,
            )

            if payload["iss"] != self.issuer:
                return User(False)

            return User(True, payload["sub"], payload.get("name"), payload.get("email"))

        except jwt.ExpiredSignatureError:
            return User(False)

        except jwt.JWTError:
            return User(False)


# Use the API_SECRET from the environment variables
app.config["API_SECRET"] = os.environ.get("API_SECRET")

# Pass PROJECT_ID as a context variable to templates
app.config["PROJECT_ID"] = os.environ.get("PROJECT_ID")

session = Session(app, short_session_cookie_name, issuer, jwks_uri)


@app.route("/")
def login():
    return render_template("login.html", PROJECT_ID=app.config["PROJECT_ID"])


@app.route("/home")
def home():
    user = session.get_current_user()

    if user.is_valid:
        user_data = {"id": user.sub, "name": user.name, "email": user.email}
        return render_template(
            "home.html", user_data=user_data, PROJECT_ID=app.config["PROJECT_ID"]
        )
    else:
        raise Unauthorized()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
