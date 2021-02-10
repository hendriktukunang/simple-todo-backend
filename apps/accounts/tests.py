from apps.commons.unitests import SerializedApiRequestUnitest
from .views import Auth


class AuthWithCorrectCredentialsTest(SerializedApiRequestUnitest, Auth):

    payload = {
        "username": "hendrik@blankontech.com",
        "password": "123456",
    }
    expected_response = {
        "token": "<any>",
        "first_name": "Hendrik",
        "last_name": "Tukunang",
        "email": "hendrik@blankontech.com",
        "created_at": None,
        "last_updated_at": None,
    }
    rule = {"token": {"ignore": True}, "created_at": {"ignore": True}}


class AuthWithIncorrectCredentialsTest(SerializedApiRequestUnitest, Auth):

    payload = {
        "username": "hendrik@blankontech.com",
        "password": "1234567",
    }
    expected_response = {
        "non_field_errors": ["Unable to log in with provided credentials."]
    }
    rule = {}
