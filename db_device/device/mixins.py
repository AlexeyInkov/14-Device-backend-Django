from rest_framework import status
from rest_framework.response import Response


class CreateModelViewSetMixin:
    def create(self, request, *args, **kwargs):
        instance = self.queryset.filter(**request.data.dict()).first()
        if instance:
            serializer = self.serializer_class(instance)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
