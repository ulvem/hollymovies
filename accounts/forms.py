from django.contrib.auth.forms import (
  AuthenticationForm, PasswordChangeForm, UserCreationForm
)
from django.db.transaction import atomic
from django.forms import CharField, Textarea, Select

from accounts.models import Profile


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ['username', 'first_name', 'email']

    biography = CharField(
        label='Biography',
        widget=Textarea(attrs={'placeholder': 'Tell us your story with movies'}),
        min_length=20
    )

    gender = CharField(
        widget=Select(
            choices=[
                ("M", 'Male'),
                ("F", 'Female'),
            ]
        )
    )

    @atomic
    def save(self, commit=True):
        self.instance.is_active = True
        result = super().save(commit)
        biography = self.cleaned_data['biography']
        gender = self.cleaned_data['gender']
        profile = Profile(biography=biography, user=result, gender=gender)
        if commit:
            profile.save()
        return result
