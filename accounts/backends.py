from .models import Profile


class EmailBackend(object):

    def authenticate(self, email=None, password=None, **kwargs):
        try:
            user = Profile.objects.get(email=str(email))
            if user.check_password(password):
                return user, ''
            else:
                return None, 'Password error'
        except Profile.DoesNotExist:
            return None, 'User with this Email ' + email + ' not exists'

    def get_user(self, user_id):
        try:
            return Profile.objects.get(pk=user_id)
        except Profile.DoesNotExist:
            return None