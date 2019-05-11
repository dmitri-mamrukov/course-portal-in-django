from django.contrib.auth.models import User


def set_up_admin():
    return User.objects.create_user(username='test-admin',
                                    password='test-admin-password')

def clean_up_admin(admin_user, client):
    client.force_authenticate(user=None)
    admin_user.delete()
