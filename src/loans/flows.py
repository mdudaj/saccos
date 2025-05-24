# -*- encoding: utf-8 -*-

from viewflow import this
from viewflow.workflow import flow
from viewflow.workflow.flow.views import CreateProcessView, UpdateProcessView

from .forms import LoanApplicationForm, LoanApplicationReviewForm, LoanDocumentForm
from .helpers import get_committee_member, get_committee_members, get_role_user
from .models import LoanApplication, LoanApprovalProcess, LoanDocument


class LoanApprovalFlow(flow.Flow):
    """
    Flow for loan approval.
    """
    process_class = LoanApprovalProcess
    process_title = "Loan Approval"
    process_description = "Upload document, enter application data, and review step-by-step"

    # Step 0 - Start Process
    
    start = (
        flow.Start(CreateProcessView.as_view(form_class=LoanDocumentForm))
        .Permission('loans.add_loandocument')
        .Next(this.upload_complete)
    )

    # Step 1 - Assign to uploader (loan officer)
    upload_complete = (
        flow.View(UpdateProcessView.as_view(form_class=LoanDocumentForm))
        .Assign(lambda activation: get_role_user('Loan Officer'))
        .Permission('loans.add_loandocument')
        .Next(this.fill_application_data)
    )


    # Step 2 - Fill Loan Application Data
    fill_application_data = (
        flow.View(UpdateProcessView.as_view(form_class=LoanApplicationForm))
        .Assign(lambda activation: activation.user)
        .Permission('loans.change_loanapplication')
        .Next(this.accountant_review)
    )

    # Step 3 - Accountant Review
    accountant_review = (
        flow.View(UpdateProcessView.as_view(form_class=LoanApplicationReviewForm))
        .Assign(lambda activation: get_role_user('Accountant'))
        .Next(this.committee_review_1)
    )

    # Step 4 - Committee Review
    committee_review_1 = (
        flow.View(UpdateProcessView.as_view(form_class=LoanApplicationReviewForm))
        .Assign(lambda activation: get_committee_member(0))
        .Next(this.committee_review_2)
    )

    committee_review_2 = (
        flow.View(UpdateProcessView.as_view(form_class=LoanApplicationReviewForm))
        .Assign(lambda activation: get_committee_member(1))
        .Next(this.chairman_review)
    )

    # Step 5 - Chairman Review
    chairman_review = (
        flow.View(UpdateProcessView.as_view(form_class=LoanApplicationReviewForm))
        .Assign(lambda activation: get_role_user('chairman'))
        .Next(this.set_final_status)
    )

    set_final_status = (
        flow.Function(this.set_status).Next(this.end)
    )

    end = flow.End()

    def set_status(self, activation):
        """
        Set the final status of the loan application based on the committee's decision.
        
        Args:
            activation: The current activation of the flow.
        """
        application = activation.process.artifact
        if application.status == 'approved':
            application.process.approved = True
        application.save()