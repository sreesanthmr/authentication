from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class PhoneOTPBackend(BaseBackend):

    def authenticate(self, request, otp=None, **kwargs):
        try:
            # Find the user by phone number
            user = User.objects.get(otp=otp)

            # Verify OTP (replace with your OTP verification logic)
            if user.otp == otp:
                user.otp = None
                user.save()
                return user
            else:
                raise ValidationError("Invalid OTP")
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
