from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class RegisterForm(UserCreationForm):
    class Meta:
        User = get_user_model()
        model = User
        fields = ('username', 'email', 'password1', 'user_gender', 'user_postcode', 'user_phone_number')