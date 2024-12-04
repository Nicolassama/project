from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

User = get_user_model()


class SignUpForm(UserCreationForm):
    usable_password = None

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class LoginFrom(AuthenticationForm):
    class Meta:
        model = User