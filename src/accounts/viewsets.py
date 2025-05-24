# -*- encoding: utf-8 -*-

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.utils.translation import gettext_lazy as _
from viewflow import Icon
from viewflow.forms import FieldSet, Layout, Row
from viewflow.urls import Application, DeleteViewMixin, DetailViewMixin, ModelViewset

User = get_user_model()


class UserViewset(DeleteViewMixin, DetailViewMixin, ModelViewset):
    """
    Manager system users (Administrators, Loan Officers, Secretariate committee, etc.)
    """
    icon = Icon('person')
    model = User
    list_columns = ('email', 'first_name', 'last_name', 'is_active', 'is_staff')
    list_search_fields = ('email', 'first_name', 'last_name')
    list_filter_fields = ('is_active', 'is_staff')

    queryset = User.objects.filter(is_staff=True).order_by('-created')

    form_layout = Layout(
        "email",
        FieldSet(
            _("Personal Information"),
            Row('first_name', 'last_name'),
        ),
        FieldSet(
            _("Account Settings"),
            Row('is_active', 'is_staff'),
        ),
        FieldSet(
            _("Permissions"),
            Row('groups'),
        ),
    )


class GroupViewset(DeleteViewMixin, DetailViewMixin, ModelViewset):
    """
    Manages roles and permissions for users.
    """
    icon = Icon('security')
    model = Group
    list_columns = ('name','permissions_count')
    list_searh_fields = ('name',)
    list_filter_fields = ('permissions',)
    
    queryset = Group.objects.prefetch_related('permissions').order_by('name')

    def permissions_count(self, obj):
        """
        Returns the number of permissions associated with the group.
        """
        return obj.permissions.count()
    permissions_count.short_description = _("Permissions Count")

    form_layout = Layout(
        "name",
        FieldSet(
            _("Permissions"),
            Row('permissions'),
        ),
    )
    

class UserAdminApp(Application):
    """
    User management application.
    """
    title = _("User Management")
    app_name = "accounts"
    icon = Icon('people')

    viewsets = [
        UserViewset(),
        GroupViewset(),
    ]

        
