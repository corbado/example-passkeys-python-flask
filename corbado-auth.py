from typing import List
from corbado_python_sdk.entities.session_validation_result import (
    SessionValidationResult,
)
from corbado_python_sdk.generated.models.identifier import Identifier
from flask import Flask, render_template, request
from werkzeug.exceptions import Unauthorized
from dotenv import load_dotenv
import os
from corbado_python_sdk import (
    Config,
    CorbadoSDK,
    IdentifierService,
    UserEntity,
    SessionService,
    UserService,
)

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
sessions: SessionService = sdk.sessions
identifiers: IdentifierService = sdk.identifiers
users: UserService = sdk.users

app.config["API_SECRET"] = API_SECRET
app.config["PROJECT_ID"] = PROJECT_ID

@app.route("/")
def login() -> str:
    return render_template(
        template_name_or_list="login.html", PROJECT_ID=app.config["PROJECT_ID"]
    )

@app.route("/home")
def home() -> str:
    # Acquire cookies with your preferred method
    sessionToken: str = request.cookies.get("cbo_session_token") or ""
    validation_result: SessionValidationResult = sessions.get_current_user(
        short_session=sessionToken
    )

    if validation_result.authenticated:
        user_id: str = validation_result.user_id or ""
        user: UserEntity = users.get(user_id=user_id)
        email_identifiers: List[Identifier] = identifiers.list_all_emails_by_user_id(
            user_id=user_id
        )

        user_data = {
            "id": user.user_id,
            "name": user.full_name,
            "email": email_identifiers[0].value,
        }
        return render_template(
            template_name_or_list="home.html",
            user_data=user_data,
            PROJECT_ID=app.config["PROJECT_ID"],
        )
    else:
        raise Unauthorized()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
