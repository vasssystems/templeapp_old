# webapp/features/common/custom_pagination.py
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


# Custome Pagination
class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        paginated_data = list(self.paginate_queryset(data, self.request))
        return Response({
            "status": True,
            "message": "Success",
            "data": {
                "content": paginated_data,
                "current_page": self.page.number if self.page else None,
                "total_pages": self.page.paginator.num_pages if self.page else None,
                "total_count": self.page.paginator.count if self.page else None,
                "current_page_count": len(paginated_data),
                "next": self.get_next_link(),
                "previous": self.get_previous_link()
            }
        })
