from apps.accounts.models import Token


class TokenAuthMiddleware:
    """
    Token authorization middleware for Django Channels 2
    """

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        try:
            query = dict(
                (x.split("=") for x in scope["query_string"].decode().split("&"))
            )
            token = query["token"]
            token = self.get_session(token)
            if token:
                scope["user"] = token.user
            else:
                scope["user"] = None
            return self.inner(scope)
        except:
            scope["user"] = None
            return self.inner(scope)

    def get_session(self, token):
        return Token.objects.get(key=token)
