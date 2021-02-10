from rest_framework.authentication import TokenAuthentication as RestTokenAuthentication
from apps.accounts.models import Token


class TokenAuthentication(RestTokenAuthentication):
    """
    override default token authentication from django rest and set model to our defined token class under accounts apps
    """

    model = Token
