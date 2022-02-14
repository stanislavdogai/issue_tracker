from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from issue_tracker.apps.webapp.forms import SearchForm, ProjectForm, ProjectTaskForm, ProjectDeleteForm
from issue_tracker.apps.webapp.models import Project, Task


class ProjectPage(ListView):
    model = Project
    context_object_name = "projects"
    template_name = "projects/index.html"
    paginate_by = 3
    paginate_orphans = 0

    def get(self, request, *args, **kwargs):
        self.form = self.get_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            query = Q(title__icontains=self.search_value) | Q(description__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset.order_by("title")

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

class ProjectView(DetailView):
    template_name = 'projects/view.html'
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = self.object.tasks.order_by("-created_at")
        context['tasks'] = tasks
        return context

class CreateProject(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/create.html'

    def get_success_url(self):
        return reverse('webapp:project_view', kwargs={'pk':self.object.pk})

class ProjectTaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'projects/create.html'
    form_class = ProjectTaskForm

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        task = form.save(commit=False)
        task.project = project
        task.save()
        form.save_m2m()
        return redirect('webapp:project_view', pk=project.pk)

class UpdateProject(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/update.html'

    def get_success_url(self):
        return reverse('webapp:project_view', kwargs={'pk' : self.object.pk})

class DeleteProject(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = 'projects/delete.html'
    context_key = 'project'
    success_url = reverse_lazy('webapp:project_page')
    form_class = ProjectDeleteForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == "POST":
            kwargs['instance'] = self.object
        return kwargs