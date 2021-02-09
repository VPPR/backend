def user_helper(user) -> dict:
    return {
        'id' : str(user['_id']),
        'fullname' : user['fullname'],
        'email' : user['email'],
        'phone_number' : user['phone'],
        'is_admin' : user['is_admin']
    }

# def admin_helper(admin) -> dict:
#     return {
#         'id' : str(admin['_id']),
#         'fullname' : admin['fullname'],
#         'email' : admin['email'],
#         'is_admin' : admin['is_admin']
#     }