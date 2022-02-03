from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from webapp.models import Task
from django.views.generic import TemplateView, FormView, ListView, DetailView, CreateView, UpdateView
from webapp.forms import TaskForm, TaskFormDelete, SearchForm


class HomePage(ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "tasks/index.html"
    paginate_by = 10
    paginate_orphans = 0

    def get(self, request, *args, **kwargs):
        self.form = self.get_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            query = Q(summary__icontains=self.search_value) | Q(description__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset.order_by("summary")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = SearchForm()
        if self.search_value:
            context['search'] = self.search_value
        return context

    def get_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get("search")


class TaskView(DetailView):
    template_name = 'tasks/view.html'
    model = Task


class CreateTask(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create.html'

    def get_success_url(self):
        return reverse('view_page', kwargs={'pk':self.object.pk})


class UpdateTask(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/update.html'

    def get_success_url(self):
        return reverse('view_page', kwargs={'pk' : self.object.pk})

class DeleteTask(TemplateView):
    CONFIRM = 'ДА'
    def get(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs.get('pk'))
        form = TaskFormDelete()
        return render(request, 'tasks/delete.html', {'task': task, 'form': form})

    def post(self, request, *args, **kwargs):
        form = TaskFormDelete(data=request.POST)
        task = get_object_or_404(Task, pk=kwargs.get('pk'))
        if form.is_valid():
            if form.cleaned_data.get('confirm') != self.CONFIRM:
                form.errors['confirm'] = ['Вы ввели другое слово']
                return render(request, 'tasks/delete.html', {'form': form, 'task': task})
            task.delete()
            return redirect('home_page')
        return render(request, 'tasks/delete.html', {'form': form, 'task': task})