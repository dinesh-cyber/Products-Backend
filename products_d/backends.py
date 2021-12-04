from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from products_d.users.models import User

UserModel = get_user_model()


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None):
        if "@" in username:
            kwargs = {"email": username.lower()}
        else:
            kwargs = {"username": username}
        try:
            user = UserModel.objects.get(**kwargs)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            UserModel().set_password(password)

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None