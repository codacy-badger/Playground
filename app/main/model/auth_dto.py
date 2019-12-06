from flask_restplus import Namespace, fields


class AuthDto:
    api = Namespace("auth", description="authentication related operations")
    user_auth = api.model(
        "Authentication details",
        {
            "email": fields.String(required=True, description="The email address"),
            "password": fields.String(required=True, description="The user password "),
        },
    )
