# -*- encoding: utf-8 -*-

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from viewflow import Icon
from viewflow.forms import FieldSet, Layout, Row
from viewflow.urls import Application, DeleteViewMixin, DetailViewMixin, ModelViewset

from .forms import MemberProfileForm
from .models import LoanAccount, MemberProfile, SavingsAccount

User = get_user_model()


class MemberProfileViewset(DeleteViewMixin, DetailViewMixin, ModelViewset):
    """
    Manage member profiles.
    """

    icon = Icon('person')
    model = MemberProfile
    form_class = MemberProfileForm
    list_columns = ('user_email', 'user_first_name', 'user_last_name', 'membership_number', 'joined_date')
    list_search_fields = ('user_email', 'user_first_name', 'user_last_name', 'membership_number')
    list_filter_fields = ('joined_date',)
    
    queryset = MemberProfile.objects.all()
    ordering = ('-joined_date',)

    def user_email(self, obj):
        return obj.user.email if obj.user else None
    user_email.short_description = _("Email")

    def user_first_name(self, obj):
        return obj.user.first_name if obj.user else None
    user_first_name.short_description = _("First Name")

    def user_last_name(self, obj):
        return obj.user.last_name if obj.user else None
    user_last_name.short_description = _("Last Name")

    
    form_layout = Layout(
        "email",
        FieldSet(
            _("Personal Information"),
            Row('first_name', 'last_name'),
        ),
        FieldSet(
            _("Membership Information"),
            Row('membership_number', 'phone_number'),
            Row('joined_date')
        ),
    )


class MembershipApp(Application):
    """
    Membership management application.
    """
    title = _("Membership Management")
    app_name = 'membership'
    icon = Icon('verified_user')
    default_view = MemberProfileViewset

    viewsets = [
        MemberProfileViewset(),
    ]
