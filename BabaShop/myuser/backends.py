from django.contrib.auth.backends import ModelBackend
from myuser.models import CustomUser
from django.db.models import Q


UserModel = CustomUser


class AuthBackend(ModelBackend): # user can login with phone username or Email
    def authenticate(self, request, phone=None, password=None, **kwargs):
        try:
            user = UserModel.objects.get(Q(username__iexact=phone) | Q(email__iexact=phone) | Q(phone__iexact=phone))
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
            return
        except UserModel.MultipleObjectsReturned:
            user = UserModel.objects.filter(Q(username__iexact=phone) | Q(email__iexact=phone) | Q(phone__iexact=phone)).order_by('id').first()

        if user.check_password(password) and self.user_can_authenticate(user):
            return user