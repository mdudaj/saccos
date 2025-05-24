# -- coding: utf-8 -*-

from django.contrib.auth import get_user_model
from django.urls import path
from viewflow.contrib.auth import AuthViewset
from viewflow.urls import Application, ModelViewset, Site

from accounts.viewsets import UserAdminApp
from loans.viewsets import LoanApprovalApp
from membership.viewset import MembershipApp


class SaccosSite(Site):
    """
    Custom site for NIMR SACCOS LTD.
    This site includes various applications and viewsets for managing users, loans, and memberships.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = "NIMR SACCOS LTD."
        self.primary_color = "#00ACED"
        self.secondary_color = "#144B9D"
        self.base_template_name = "layouts/base_page.html"

site = SaccosSite(

    viewsets=[
        UserAdminApp(),
        MembershipApp(),
        LoanApprovalApp(),
])

urlpatterns = [
    path('accounts/', AuthViewset(with_profile_view=True).urls),
    path('', site.urls),
]
