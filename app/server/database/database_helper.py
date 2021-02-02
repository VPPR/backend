def user_helper(user) -> dict:
    return {
        "id": str(user['_id']),
        "fullname": user['fullname'],
        "email": user['email'],
        "phone": user['phone']
    }

def admin_helper(admin) -> dict:
    return {
        "id": str(admin['_id']),
        "fullname": admin['fullname'],
        "email": admin['email'],
    }