from django import forms
from priority.models import Priority
from tasks.models import Tasks


class UpdateTaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ["title", "description", "secuence"]

    title = forms.CharField(max_length=255, required=True)
    description = forms.CharField(max_length=255, required=True)
    secuence = forms.IntegerField(required=True)
    user_id = forms.CharField(required=True)

    priority = forms.ModelChoiceField(queryset=Priority.objects.all(), required=False)
    priority_id = forms.CharField(required=False)

    def clean(self):
        cleaned_data = super().clean()

        user_id = cleaned_data.get("user_id")
        priority_id = cleaned_data.get("priority_id")

        if priority_id == "":
            data = {}
            for key, value in cleaned_data.items():
                if value is None or value == "":
                    continue
                data[key] = value
            return data

        priority_belong_user = Priority.objects.filter(
            id=priority_id, user_id=user_id
        ).first()
        if priority_belong_user is None:
            raise forms.ValidationError(
                {"priority_id": ["Priority Id does not belong to user"]}
            )

        cleaned_data["priority"] = priority_belong_user

        return cleaned_data
