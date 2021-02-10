from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class BoundToUserMixin:
    """
    Same analogy with bound to user model,
    we operate user field inside this mixin,
    since it extended inside views, we override the payload and queryset
    where in payload we add user key from auth data, and for queryset
    we filter with condition user = auth.user
    """

    bound_to_user_field_name = "user"

    def initial(self, request, *args, **kwargs):
        """
        we add user data to request.data on initial function
        this way will be more efficient rather than define
        it in each request, or FE define it in  payload
        :param request: request object
        :param args: list of args
        :param kwargs: dict of kwargs
        :return: super method
        """
        try:
            request.data["user"] = request.auth.user
        except:
            pass
        return super(BoundToUserMixin, self).initial(request, *args, **kwargs)

    def get_queryset(self):
        """
        we define queryset by filter a data owned by current active user,
        we use this for all model extends bound to user, like todo model
        :return: qs filtered with owned by user condition
        """
        filter_kwargs = {self.bound_to_user_field_name: self.request.auth.user}
        return super(BoundToUserMixin, self).get_queryset().filter(**filter_kwargs)

    def get_serializer(self, *args, **kwargs):
        if "exclude_fields" in kwargs:
            kwargs["exclude_fields"].append("user")
        else:
            kwargs["exclude_fields"] = [
                "user",
            ]
        return super(BoundToUserMixin, self).get_serializer(*args, **kwargs)


class OrderingSupportMixin:
    """
    this mixin will allow api to be ordered by any fields for it's model
    """

    filter_backends = [OrderingFilter]
    ordering_fields = "__all__"


class BaseQuerysetMixin:
    """
    BaseQuerysetMixin is t prevent inconsistent order,
    basically in serialized view, we need a queryset, but since by default
    it will do objects.all(), django will send alert that we might have inconsistent data,
    since no sort on it, so if there's no ordering fields found in request, by default
    we will sort queryset by id
    """

    def __init__(self, *args, **kwargs):
        serializer_class_object = self.serializer_class()
        self.queryset = serializer_class_object.Meta.model.objects.all()

    def get_queryset(self):
        """
        if no ordering fields set in GET params, then we use id as default orde
        :return: qs data ordered by ID or defined field
        """
        rs = super(BaseQuerysetMixin, self).get_queryset()
        if self.request.GET.get("ordering") is None:
            rs = rs.order_by("id")
        return rs
