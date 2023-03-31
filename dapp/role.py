class UserRole:
    ADMIN_ID = 1
    ADMIN = 'admin'
    VOTER = 'voter'


def is_admin(user):
    if user.id == UserRole.ADMIN_ID:
        return True
    return False
