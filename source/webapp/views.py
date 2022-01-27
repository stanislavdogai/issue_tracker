from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from webapp.models import Task
from django.views import View
from django.views.generic import TemplateView, RedirectView, FormView, ListView
from webapp.forms import TaskForm, TaskFormDelete, SearchForm
from webapp.base import FormView as CustomFormView



class HomePage(ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "index.html"
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



class TaskView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = get_object_or_404(Task, pk=kwargs.get("pk"))
        context['task'] = task
        return context



class CreateTask(CustomFormView):
    form_class = TaskForm
    template_name = 'create_task.html'

    def form_valid(self, form):
        # types = form.cleaned_data.pop('types')
        # self.object = Task.objects.create(**form.cleaned_data)
        # self.object.types.set(types)
        self.object = form.save()
        return super().form_valid(form)

    def get_redirect_url(self):
        return redirect('view_page', pk=self.object.pk)



class UpdateTask(FormView):
    form_class = TaskForm
    template_name = 'update_task.html'

    def dispatch(self, request, *args, **kwargs):
        self.task = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = self.task
        return context

    # def get_initial(self):
    #     initial = {}
    #     for key in 'summary', 'description', 'status':
    #         initial[key] = getattr(self.task, key)
    #     initial['types'] = self.task.types.all()
    #     return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.task
        return kwargs

    def form_valid(self, form):
        # types = form.cleaned_data.pop('types')
        # for key, value in form.cleaned_data.items():
        #     if value is not None:
        #         setattr(self.task, key, value)
        # self.task.save()
        # self.task.types.set(types)
        self.task = form.save()
        return super(UpdateTask, self).form_valid(form)

    def get_success_url(self):
        return reverse('view_page', kwargs={'pk': self.task.pk})

    def get_object(self):
        return get_object_or_404(Task, pk=self.kwargs.get('pk'))


class DeleteTask(TemplateView):
    CONFIRM = 'ДА'
    def get(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs.get('pk'))
        form = TaskFormDelete()
        return render(request, 'delete.html', {'task': task, 'form': form})

    def post(self, request, *args, **kwargs):
        form = TaskFormDelete(data=request.POST)
        task = get_object_or_404(Task, pk=kwargs.get('pk'))
        if form.is_valid():
            if form.cleaned_data.get('confirm') != self.CONFIRM:
                form.errors['confirm'] = ['Вы ввели другое слово']
                return render(request, 'delete.html', {'form': form, 'task': task})
            task.delete()
            return redirect('home_page')
        return render(request, 'delete.html', {'form': form, 'task': task})

