from rest_framework.pagination import (PageNumberPagination)

class MessagesPageNumberPagination(PageNumberPagination):
	page_size = 20