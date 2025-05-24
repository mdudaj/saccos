# -*- encoding: utf-8 -*-

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import LoanAccount, MemberProfile, SavingsAccount


@receiver(post_save, sender=MemberProfile)
def create_savings_account(sender, instance, created, **kwargs):
    """
    Create a savings account for the member when their profile is created.
    """
    if created:
        SavingsAccount.objects.create(member=instance)

@receiver(post_save, sender=MemberProfile)
def create_loan_account(sender, instance, created, **kwargs):
    """
    Create a loan account for the member when their profile is created.
    """
    if created:
        LoanAccount.objects.create(member=instance)

@receiver(post_save, sender=MemberProfile)
def save_savings_account(sender, instance, **kwargs):
    """
    Save the savings account when the member profile is saved.
    """
    instance.savings_accounts.all().update(member=instance)

@receiver(post_save, sender=MemberProfile)
def save_loan_account(sender, instance, **kwargs):
    """
    Save the loan account when the member profile is saved.
    """
    instance.loan_accounts.all().update(member=instance)

