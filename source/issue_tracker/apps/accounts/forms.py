from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class MyUserCreateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput, strip=False)
    password_confirm = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        if password != password_confirm:
            raise ValidationError("Пароли не совпадают")
        if not first_name and not last_name:
            raise ValidationError('Введите хотя бы имя или фамилию')
        return cleaned_data


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get("password"))
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'password', 'password_confirm', 'email', 'first_name', 'last_name')