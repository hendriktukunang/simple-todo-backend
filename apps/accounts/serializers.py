from apps.commons.serializers import BaseModelSerializer
from apps.accounts.models import User


class UserSerializer(BaseModelSerializer):
    def __init__(self, *args, **kwargs):
        self.Meta.fields = [
            "first_name",
            "last_name",
            "email",
        ]
        super(UserSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = []
