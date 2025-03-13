from .servises.request_services import get_tso_selected, get_org_selected, get_cust_selected, get_mu_selected


class TemplateMixin:
    def get_template_names(self):
        if self.request.headers.get("Hx-Request"):
            template_name = self.template_name
        else:
            template_name = "frontend/index.html"
        return template_name


class ContextDataMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["org_selected"] = get_org_selected(self.request)
        context["tso_selected"] = get_tso_selected(self.request)
        context["cust_selected"] = get_cust_selected(self.request)
        context["mu_selected"] = get_mu_selected(self.request)
        return context
