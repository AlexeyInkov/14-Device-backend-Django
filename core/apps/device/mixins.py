from rest_framework import status
from rest_framework.response import Response

from apps.device.servises.request_services import (
    get_tso_selected,
    get_org_selected,
    get_cust_selected,
    get_mu_selected,
)


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


class TemplateMixin:
    def get_template_names(self):
        if self.request.headers.get("Hx-Request"):
            template_name = self.template_name
        else:
            template_name = "device/index.html"
        return template_name


class ContextDataMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["org_selected"] = get_org_selected(self.request)
        context["tso_selected"] = get_tso_selected(self.request)
        context["cust_selected"] = get_cust_selected(self.request)
        context["mu_selected"] = get_mu_selected(self.request)
        return context
