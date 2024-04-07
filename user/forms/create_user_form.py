from django import forms
from user.models import User

class CreateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'id'
        ]

    id = forms.CharField(max_length=10, required=True, min_length=10)