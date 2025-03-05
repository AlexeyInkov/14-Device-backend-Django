from django.http import HttpRequest


def get_org_selected(request: HttpRequest) -> str | None:
    org_selected_request = request.GET.get("organization")
    org_selected = request.session.get("org_selected")
    if org_selected_request != org_selected:
        reset_tso_selected(request)
        reset_cust_selected(request)
        reset_mu_selected(request)

        request.session["org_selected"] = org_selected_request
        return org_selected_request
    return org_selected


def get_tso_selected(request: HttpRequest) -> str:
    tso_selected_request = request.GET.get("tso")
    tso_selected = request.session.get("tso_selected")
    if tso_selected_request != tso_selected and tso_selected_request is not None:
        reset_cust_selected(request)
        reset_mu_selected(request)

        request.session["tso_selected"] = tso_selected_request
        return tso_selected_request
    return tso_selected


def get_cust_selected(request: HttpRequest) -> str:
    cust_selected_request = request.GET.get("customer")
    cust_selected = request.session.get("cust_selected")
    if cust_selected_request != cust_selected and cust_selected_request is not None:
        reset_mu_selected(request)

        request.session["cust_selected"] = cust_selected_request
        return cust_selected_request
    return cust_selected


def get_mu_selected(request: HttpRequest) -> int:
    mu_selected_request = request.GET.get("metering_unit")
    mu_selected = request.session.get("mu_selected")
    if mu_selected_request is not None:
        request.session["mu_selected"] = mu_selected_request
        return mu_selected_request
    return mu_selected


def reset_org_selected(request: HttpRequest) -> None:
    request.session["org_selected"] = None


def reset_tso_selected(request: HttpRequest) -> None:
    request.session["tso_selected"] = None


def reset_cust_selected(request: HttpRequest) -> None:
    request.session["cust_selected"] = None


def reset_mu_selected(request: HttpRequest) -> None:
    request.session["mu_selected"] = None
