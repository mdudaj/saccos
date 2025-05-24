# -*- encoding: utf-8 -*-

from django import forms
from django.contrib.auth import get_user_model
from django.forms.models import inlineformset_factory
from django.utils.translation import gettext_lazy as _
from viewflow.forms import ModelForm

from .models import LoanAccount, MemberProfile, SavingsAccount, Transaction

User = get_user_model()


class MemberProfileForm(ModelForm):
    """
    Form for creating membership information.
    """
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        required=True,
        help_text=_("Email address of the member.")
    )
    first_name = forms.CharField(
        label=_("First Name"),
        max_length=30,
        required=True,
        help_text=_("First name of the member.")
    )
    last_name = forms.CharField(
        label=_("Last Name"),
        max_length=30,
        required=True,
        help_text=_("Last name of the member.")
    )

    def save(self, commit=True):
        """
        Save membership information to the database.
        """
        # Create a new MemberProfile instance
        membership = super().save(commit=False)

        # Create or update the user profile
        user, created = User.objects.update_or_create(
            email=self.cleaned_data['email'],
            defaults={
                'first_name': self.cleaned_data['first_name'],
                'last_name': self.cleaned_data['last_name']
            }
        )

        # Associate the user with the membership
        if created:
            membership.user = user
        else:
            # If the user already exists, update the membership with the existing user
            membership.user = User.objects.get(email=self.cleaned_data['email'])

        # Save the membership profile
        if commit:
            membership.save()
            self.save_m2m()

        return membership

    class Meta:
        model = MemberProfile
        fields = ['membership_number', 'phone_number', 'joined_date']


