from typing import Any
from django import forms
from tasks.models import Tasks
from user.models import User
from priority.models import Priority
from steps.models import Steps


class CreateTaskFrom(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ["title", "description", "secuence", "user", "priority", "step"]

    title = forms.CharField(max_length=255, required=True)
    description = forms.CharField(max_length=255, required=True)
    secuence = forms.CharField(max_length=255, required=True)

    user = forms.ModelChoiceField(queryset=User.objects.all(),required=False)
    priority = forms.ModelChoiceField(queryset=Priority.objects.all(), required=False)
    step = forms.ModelChoiceField(queryset=Steps.objects.all(), required=False)

    user_id = forms.CharField(required=True)
    priority_id = forms.CharField(required=True)
    step_id = forms.CharField(required=True)

    def clean(self):
        cleaned_data = super().clean()
        
        user_id = cleaned_data.get("user_id")
        priority_id = cleaned_data.get("priority_id")
        step_id = cleaned_data.get("step_id")

        user_exist = User.objects.filter(id=user_id).first()
        if user_exist is None:
            raise forms.ValidationError({"user_id": ["User Id does not not exist"]})

        priority_belong_user = Priority.objects.filter(
            id=priority_id, user_id=user_id
        ).first()
        if priority_belong_user is None:
            raise forms.ValidationError(
                {"priority_id": ["Priority Id does not belong to user"]}
            )

        step_belong_user = Steps.objects.filter(id=step_id, user_id=user_id).first()
        if step_belong_user is None:
            raise forms.ValidationError(
                {"step_id": ["Step Id does not belong to user"]}
            )

        cleaned_data["user"] = user_exist
        cleaned_data["priority"] = priority_belong_user
        cleaned_data["step"] = step_belong_user
        
        return cleaned_data
