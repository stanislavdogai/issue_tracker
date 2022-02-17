from django import forms
from django.core.exceptions import ValidationError
from issue_tracker.apps.webapp.models import Task, Project


class ProjectDeleteForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ("title",)

    def clean_title(self):
        print(self.instance.title, self.cleaned_data.get("title"))
        if self.instance.title != self.cleaned_data.get("title"):
            print('error')
            raise ValidationError("Название проекта не соответствует")
        return self.cleaned_data.get("title")

class TaskDeleteForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("summary",)

    def clean_summary(self):
        print(self.instance.summary, self.cleaned_data.get("summary"))
        if self.instance.summary != self.cleaned_data.get("summary"):
            raise ValidationError("Название задачи не соответствует")
        return self.cleaned_data.get("summary")

class TaskForm(forms.ModelForm):
    def __init__(self,request, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        print(Project.objects.filter(users=request.user))
        self.fields['project'].queryset = Project.objects.filter(users=request.user)

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

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['users']
        widgets = {
            'date_start' : forms.SelectDateWidget ,
            'date_end' : forms.SelectDateWidget
        }


class ProjectTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("summary", "description", 'status', 'types')
        widgets = {
            'types': forms.CheckboxSelectMultiple
        }

class ProjectUserAddForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('users',)
        widgets = {
            'users' : forms.CheckboxSelectMultiple
        }