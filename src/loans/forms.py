from django import forms
from django.utils.translation import gettext_lazy as _
from viewflow.forms import ModelForm

from .models import LoanApplication, LoanDocument


class LoanApplicationForm(ModelForm):
    """
    Form for creating or updating a loan application.
    """
    
    class Meta:
        model = LoanApplication
        fields = ['applicant', 'amount', 'term', 'interest_rate', 'purpose']
        widgets = {
            'purpose': forms.Textarea(attrs={'rows': 4, 'placeholder': _('Describe the purpose of the loan')})
        }
        help_texts = {
            'amount': _('Enter the amount applicant wish to borrow.'),
            'term': _('Enter the term in months for the loan.'),
            'interest_rate': _('Enter the interest rate as a percentage.')
        }


class LoanDocumentForm(ModelForm):
    """
    Form for uploading a document related to a loan application.
    """
    
    class Meta:
        model = LoanDocument
        fields = ['document', 'description']
        widgets = {
            'description': forms.TextInput(attrs={'placeholder': _('Document description')})
        }
        help_texts = {
            'document': _('Upload the relevant document for the loan application.')
        }


class LoanApplicationReviewForm(ModelForm):
    """
    Form for reviewing a loan application.
    """
    
    class Meta:
        model = LoanApplication
        fields = ['status']
        widgets = {
            'status': forms.RadioSelect(
                choices=[
                    ('approved', _('Approved')),
                    ('rejected', _('Rejected'))
                ]
            )
        }