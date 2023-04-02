class UserRole:
    ADMIN_ID = 1
    ADMIN = 'admin'
    VOTER = 'voter'


class AccountStatus:
    ACTIVE = True
    BLOCKED = False


class ElectionStatus:
    PUBLIC = True
    PRIVATE = False


def is_admin(user):
    if user.id == UserRole.ADMIN_ID:
        return True
    return False
