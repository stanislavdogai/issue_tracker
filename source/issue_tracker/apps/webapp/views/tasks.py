from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse, reverse_lazy

from issue_tracker.apps.webapp.models import Task
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from issue_tracker.apps.webapp.forms import TaskForm, SearchForm, TaskDeleteForm


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


class CreateTask(PermissionRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create.html'
    permission_required = 'webapp.add_task'

    def get_success_url(self):
        return reverse('webapp:view_page', kwargs={'pk':self.object.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs




class UpdateTask(PermissionRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/update.html'
    permission_required = 'webapp.change_task'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_success_url(self):
        return reverse('webapp:view_page', kwargs={'pk' : self.object.pk})

    def has_permission(self):
        return super().has_permission() and self.request.user in self.get_object().project.users.all()

class DeleteTask(PermissionRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete.html'
    context_key = 'task'
    success_url = reverse_lazy('webapp:home_page')
    form_class = TaskDeleteForm
    permission_required = 'webapp.delete_task'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == "POST":
            kwargs['instance'] = self.object
        return kwargs

    def has_permission(self):
        return super().has_permission() and self.request.user in self.get_object().project.users.all()

def jstest(request):
    return render(request, 'tasks/JS_test.html')