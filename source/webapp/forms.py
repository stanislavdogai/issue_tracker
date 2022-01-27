from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets
from webapp.models import Type, Status, Task

# class TaskForm(forms.Form):
#     summary = forms.CharField(max_length=200, required=True, label="Заголовок")
#     description = forms.CharField(max_length=2002, required=False, label="Описание", widget=widgets.Textarea(attrs={"rows": 5, "cols":50}))
#     types = forms.ModelMultipleChoiceField(queryset=Type.objects.all(), widget=forms.CheckboxSelectMultiple)
#     status = forms.ModelChoiceField(queryset=Status.objects.all())

class TaskFormDelete(forms.Form):
    confirm = forms.CharField(max_length=3, required=True, label='Подтверждение удаления')


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = []
        widgets = {
            'types' : forms.CheckboxSelectMultiple
        }

    def clean_summary(self):
        if len(self.cleaned_data.get('summary')) < 8:
            raise ValidationError(f'Длина заголовка должна быть больше 8 символов')
        return self.cleaned_data.get('summary')

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('summary') == cleaned_data.get('description'):
            raise ValidationError('Заголовок и описание не могут быть одинаковыми')
        return cleaned_data

    def clean_description(self):
        # cleaned_data = super.clean()
        if 'description' in self.cleaned_data.get('description'):
            raise ValidationError('Нельзя вводить в поле description слово "description"')
        return self.cleaned_data.get('description')

    def clean_types(self):
        print(len(self.cleaned_data.get('types')))
        if len(self.cleaned_data.get('types')) == 3:
            raise ValidationError('Нельзя выбирать все три типа')
        return self.cleaned_data.get("types")

class SearchForm(forms.Form):
    search = forms.CharField(max_length=30, required=False, label="Найти")