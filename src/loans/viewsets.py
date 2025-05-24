# -*- encode: utf-8 -*-

from django.utils.translation import gettext_lazy as _
from viewflow import Icon
from viewflow.urls import Application
from viewflow.workflow.flow.viewset import FlowAppViewset

from .flows import LoanApprovalFlow


class LoanApprovalApp(Application):
    """
    Loan approval application.
    """

    title = _("Loan Approval")
    icon = Icon('account_balance')
    description = _("Manage loan applications and approvals.")

    viewsets = [
        FlowAppViewset(LoanApprovalFlow, icon="assignment"),
        ]