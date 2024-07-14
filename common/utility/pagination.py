from rest_framework.pagination import (
    BasePagination,
    PageNumberPagination,
    LimitOffsetPagination,
    CursorPagination,
)


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = "page_size"
    max_page_size = 10000


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 1000


class PageNumberResultsSetPagination(PageNumberPagination):
    page_size_query_param = "page_size"
    max_page_size = 50
    page_query_param = "page"

    def paginate_queryset(self, queryset, request, view=None):
        model = queryset.model
        if hasattr(model, " updated_at"):
            queryset = queryset.order_by("updated_at")
        else:
            queryset = queryset.order_by("-id")
        return super().paginate_queryset(queryset, request, view)


class LimitOffsetResultsSetPagination(LimitOffsetPagination):
    default_limit = 2
    limit_query_param = "limit"
    offset_query_param = "offset"
    max_limit = 50


class CursorResultsSetPagination(CursorPagination):
    page_size = 10
    cursor_query_param = "cursor"
    ordering = "-id"


class DynamicPagination(BasePagination):
    def paginate_queryset(self, queryset, request, view=None):
        # Determine the pagination style based on the 'pagination' query parameter
        pagination_style = request.query_params.get(
            "pagination", "page_number"
        )

        paginator_classes = {
            "page_number": PageNumberResultsSetPagination,
            "limit_offset": LimitOffsetResultsSetPagination,
            "cursor": CursorResultsSetPagination,
        }

        # Default to PageNumberResultsSetPagination if the type is not specified or recognized
        paginator_class = paginator_classes.get(
            pagination_style, PageNumberResultsSetPagination
        )
        self.paginator = paginator_class()
        return self.paginator.paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        return self.paginator.get_paginated_response(data)
