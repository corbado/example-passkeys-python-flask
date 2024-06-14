from flask import Flask, render_template, request, Response
from dotenv import load_dotenv
import os
from corbado_python_sdk import Config, CorbadoSDK, UserEntity, SessionInterface


# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

PROJECT_ID: str = os.environ.get("PROJECT_ID") or ""
API_SECRET: str = os.environ.get("API_SECRET") or ""


# Config has a default values for 'short_session_cookie_name' and 'BACKEND_API'
config: Config = Config(
    api_secret=API_SECRET,
    project_id=PROJECT_ID,
)

# Initialize SDK
sdk: CorbadoSDK = CorbadoSDK(config=config)
sessions: SessionInterface = sdk.sessions

# Use the API_SECRET from the environment variables
app.config["API_SECRET"] = API_SECRET

# Pass PROJECT_ID as a context variable to templates
app.config["PROJECT_ID"] = PROJECT_ID


@app.route("/")
def login() -> str:
    return render_template(
        template_name_or_list="login.html", PROJECT_ID=app.config["PROJECT_ID"]
    )


@app.route("/home")
def home() -> str:
    # Acquire cookies with your preferred method
    token: str = request.cookies.get(config.short_session_cookie_name) or ""
    user: UserEntity = sessions.get_current_user(short_session=token)

    if user.authenticated:
        user_data = {"id": user.user_id, "name": user.name, "email": user.email}
        return render_template(
            template_name_or_list="home.html",
            user_data=user_data,
            PROJECT_ID=app.config["PROJECT_ID"],
        )
    else:
        return Response("You are not authenticated or have not yet confirmed your email.", status=401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
