# -- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.urls import path
from viewflow.contrib.auth import AuthViewset
from viewflow.urls import Application, ModelViewset, Site

from accounts.viewsets import UserAdminApp
from members import models

site = Site(title="NIMR SACCOS LTD.", viewsets=[
    UserAdminApp(),
    # Application(
    #     title="Member Management", 
    #     icon="people", 
    #     app_name="members", 
    #     viewsets=[
    #         ModelViewset(model=models.MemberProfile),
    #     ]
    # ),
])

urlpatterns = [
    path('accounts/', AuthViewset(with_profile_view=True).urls),
    path('', site.urls),
]
