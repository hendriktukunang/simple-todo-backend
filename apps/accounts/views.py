from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from apps.accounts.serializers import UserSerializer
from apps.accounts.models import Token


class Auth(ObtainAuthToken):
    """
    user can have email and password
    and this class will handle that kind of auth
    """

    permission_classes = [
        AllowAny,
    ]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token = Token.objects.create(user=user)

        return Response(
            {
                "token": token.key,
                **UserSerializer(user, many=False).data,
            }
        )
