from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class MemberProfile(models.Model):
    """
    Model representing a member's profile.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='member_profile')
    membership_number = models.CharField(max_length=30, unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    joined_date = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} - {self.membership_number}"
    
    class Meta:
        verbose_name = "Member Profile"
        verbose_name_plural = "Member Profiles"
        ordering = ['joined_date']
