from collections import OrderedDict
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class DefaultPagination(PageNumberPagination):
    """
    only use 1 pagination class as default, rather than define 1 by 1 pagination class in each view or serializer
    """

    page_size_query_param = "page_size"

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("count", self.page.paginator.count),
                    ("current", self.page.number),
                    (
                        "next",
                        None if not self.page.has_next() else self.get_next_link(),
                    ),
                    ("results", data),
                ]
            )
        )
