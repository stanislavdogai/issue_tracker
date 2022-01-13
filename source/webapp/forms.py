from django import forms
from django.forms import widgets
from webapp.models import Type, Status

class TaskForm(forms.Form):
    summary = forms.CharField(max_length=200, required=True, label="Заголовок")
    description = forms.CharField(max_length=2002, required=True, label="Описание", widget=widgets.Textarea(attrs={"rows": 5, "cols":50}))
    type = forms.ModelChoiceField(queryset=Type.objects.all())
    status = forms.ModelChoiceField(queryset=Status.objects.all())


