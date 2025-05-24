from django.contrib.auth import get_user_model

User = get_user_model()


def get_role_user(role_name: str):
    """
    Helper function to get the user role based on the role name.
    
    Args:
        role_name (str): The name of the role to retrieve.
        
    Returns:
        User: The user with the specified role, or None if not found.
    """
    try:
        return User.objects.filter(groups__name=role_name).first()
    except User.DoesNotExist:
        return None

def get_committee_member(index: int):
    """
    Helper function to get specific user with the 'committee' role by index.
    Args:
        index (int): The index of the committee member to retrieve.
    Returns:
        User: The committee member at the specified index, or None if not found.
    """
    try:
        return User.objects.filter(groups__name='Loan Committee').all()[index]
    except IndexError:
        return None
    

def get_committee_members():
    """
    Helper function to get all users with the 'committee' role.
    
    Returns:
        QuerySet: A queryset of users with the 'committee' role.
    """
    return list(User.objects.filter(groups__name='Loan Committee').all())