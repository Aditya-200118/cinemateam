from django.contrib.auth import get_user_model


class EmailAuthBackend:

    def authenticate(self, request, email=None, password=None):
        try:
            user = get_user_model().objects.get(email=email)
            if user.check_password(password):
                return user
            return None
        except (
            get_user_model().DoesNotExist,
            get_user_model().MultipleObjectsReturned,
        ):
            return None

    def get_user(self, user_id):
        try:
            return get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return None
