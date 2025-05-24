from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class MemberProfile(models.Model):
    """
    Model representing a member's profile.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='member_profile')
    membership_number = models.CharField(max_length=30, unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    joined_date = models.DateField()

    def __str__(self):
        return f"{self.user.email} - {self.membership_number}"
    
    class Meta:
        verbose_name = "Member Profile"
        verbose_name_plural = "Member Profiles"
        ordering = ['joined_date']


class SavingsAccount(TimeStampedModel):
    """
    Model representing a member's savings account.
    """
    member = models.ForeignKey(MemberProfile, on_delete=models.CASCADE, related_name='savings_accounts')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.member.user.username} - {self.account_number}"
    
    class Meta:
        verbose_name = "Savings Account"
        verbose_name_plural = "Savings Accounts"
        ordering = ['-created']


class LoanAccount(TimeStampedModel):
    """
    Model representing a member's loan account.
    """
    member = models.ForeignKey(MemberProfile, on_delete=models.CASCADE, related_name='loan_accounts')
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    repayment_period = models.IntegerField()  # in months
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.member.user.username} - {self.loan_amount}"
    
    class Meta:
        verbose_name = "Loan Account"
        verbose_name_plural = "Loan Accounts"
        ordering = ['-created']

class Transaction(TimeStampedModel):
    """
    Model representing a transaction in a member's account.
    """
    TRANSACTION_TYPES = (
        ('deposit', _('Deposit')),
        ('withdrawal', _('Withdrawal')),
        ('transfer', _('Transfer')),
    )

    account = models.ForeignKey(SavingsAccount, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.account.member.user.username} - {self.transaction_type} - {self.amount}"
    
    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ['-date']