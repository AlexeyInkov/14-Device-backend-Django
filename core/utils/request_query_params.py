import logging

from django.http import HttpRequest

logger = logging.getLogger(__name__)


def get_org_selected(request: HttpRequest) -> str:
    """
    Returns the organization selected from the request.
    If the organization is not selected, returns the last selected organization.
    If the organization is not selected and there is no last selected organization, returns None.
    """
    logger.info("Running get_org_selected")
    org_selected_request = request.GET.get("organization")
    org_selected = request.session.get("org_selected")
    logger.debug(f"org_selected_request: {org_selected_request}")
    logger.debug(f"org_selected_session: {org_selected}")
    if org_selected_request != org_selected:
        reset_selected_param(request, "tso_selected")
        reset_selected_param(request, "cust_selected")
        reset_selected_param(request, "mu_selected")
        request.session["org_selected"] = org_selected_request
        return org_selected_request
    return org_selected


def get_tso_selected(request: HttpRequest) -> str:
    """Returns the TSO selected from the request."""
    logger.info("Running get_tso_selected")
    tso_selected_request = request.GET.get("tso")
    tso_selected = request.session.get("tso_selected")
    logger.debug(f"tso_selected_request: {tso_selected_request}")
    logger.debug(f"tso_selected_session: {tso_selected}")
    if tso_selected_request != tso_selected and tso_selected_request is not None:
        reset_selected_param(request, "cust_selected")
        reset_selected_param(request, "mu_selected")
        request.session["tso_selected"] = tso_selected_request
        return tso_selected_request
    return tso_selected


def get_cust_selected(request: HttpRequest) -> str:
    """Returns the CUST selected from the request."""
    logger.info("Running get_cust_selected")
    cust_selected_request = request.GET.get("customer")
    cust_selected = request.session.get("cust_selected")
    logger.debug(f"cust_selected_request: {cust_selected_request}")
    logger.debug(f"cust_selected_session: {cust_selected}")
    if cust_selected_request != cust_selected and cust_selected_request is not None:
        reset_selected_param(request, "mu_selected")

        request.session["cust_selected"] = cust_selected_request
        return cust_selected_request
    return cust_selected


def get_mu_selected(request: HttpRequest) -> int:
    """Returns the MU selected from the request."""
    logger.info("Running get_mu_selected")
    mu_selected_request = request.GET.get("metering_unit")
    mu_selected = request.session.get("mu_selected")
    logger.debug(f"mu_selected_request: {mu_selected_request}")
    logger.debug(f"mu_selected_session: {mu_selected}")
    if mu_selected_request is not None:
        request.session["mu_selected"] = mu_selected_request
        return mu_selected_request
    return mu_selected


def reset_selected_param(request: HttpRequest, param_name: str) -> None:
    """Resets the selected parameter from the request."""
    logger.info(f"resetting {param_name}")
    param = request.session.pop(param_name, None)
    logger.debug(f"reset {param_name} = {param}")
    logger.debug(f"org_selected_session: {request.session.get('org_selected')}")
