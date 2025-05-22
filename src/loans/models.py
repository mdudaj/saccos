from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class LoanApplication(TimeStampedModel):
    """
    Model representing a loan application.
    """
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loan_applications')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', _('Pending')),
            ('approved', _('Approved')),
            ('rejected', _('Rejected')),
        ],
        default='pending'
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
