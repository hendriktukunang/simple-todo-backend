from rest_framework.serializers import ModelSerializer, SerializerMethodField


class BaseModelPropertySerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop("exclude_fields", None)
        super(BaseModelPropertySerializer, self).__init__(*args, **kwargs)
        if remove_fields:
            # for multiple fields in a list
            for field_name in remove_fields:
                self.fields.pop(field_name)

    def get_request_context(self):
        return self.context.get("request")


class BaseModelSerializer(BaseModelPropertySerializer):
    def __init__(self, *args, **kwargs):
        if "created_at" not in self.Meta.fields:
            self.Meta.fields.append("created_at")

        if "last_updated_at" not in self.Meta.fields:
            self.Meta.fields.append("last_updated_at")

        super(BaseModelSerializer, self).__init__(*args, **kwargs)

    class Meta:
        extra_kwargs = {
            "created_at": {"read_only": True},
            "last_updated_at": {"read_only": True},
        }


class BoundToUserSerializer(BaseModelPropertySerializer):
    def validate(self, attrs):
        request_context = self.get_request_context()
        attrs["user"] = request_context.data.get("user")
        return attrs

    def __init__(self, *args, **kwargs):
        if "user" not in self.Meta.fields:
            self.Meta.fields.append("user")
        return super(BoundToUserSerializer, self).__init__(*args, **kwargs)
