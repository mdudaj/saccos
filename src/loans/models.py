# -*- encoding: utf-8 -*-

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from viewflow import jsonstore
from viewflow.workflow.models import Process

User = get_user_model()

from membership.models import MemberProfile


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class LoanApplication(TimeStampedModel):
    """
    Model representing a loan application.
    """
    applicant = models.ForeignKey(MemberProfile, on_delete=models.CASCADE, related_name='loan_applications')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    term = models.PositiveIntegerField(help_text=_("Term in months"))
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, help_text=_("Interest rate in percentage"))
    purpose = models.TextField(help_text=_("Purpose of the loan"))
    status = models.CharField(
        max_length=20,
        choices=[
            ('new', _('New')),
            ('pending', _('Pending')),
            ('approved', _('Approved')),
            ('rejected', _('Rejected')),
        ],
        default='new'
    )

    def __str__(self):
        return f"Loan Application by {self.applicant.username} - {self.status}"
    
    class Meta:
        verbose_name = "Loan Application"
        verbose_name_plural = "Loan Applications"
        ordering = ['-created']


class LoanDocument(TimeStampedModel):
    """
    Model representing a document related to a loan application.
    """
    application = models.ForeignKey(LoanApplication, on_delete=models.CASCADE, related_name='documents')
    document = models.FileField(upload_to='loan_documents/')
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Document for {self.application} - {self.description}"
    
    class Meta:
        verbose_name = "Loan Document"
        verbose_name_plural = "Loan Documents"
        ordering = ['-created']


class LoanApprovalProcess(Process):
    """
    Workflow process for loan application approval.
    """
    artifact: LoanApplication

    approved = jsonstore.BooleanField(default=False)

    class Meta:
        proxy = True
