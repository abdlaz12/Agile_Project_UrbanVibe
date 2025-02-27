from django.contrib.auth.backends import ModelBackend
from WebPage.models import CustomUser  # Sesuaikan dengan model yang digunakan

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return None
        
        if user.check_password(password):
            return user
        return None