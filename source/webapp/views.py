from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from webapp.models import Task
from django.views import View
from django.views.generic import TemplateView, RedirectView, FormView
from webapp.forms import TaskForm, TaskFormDelete
from webapp.base import FormView as CustomFormView



class HomePage(TemplateView):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = Task.objects.order_by("summary")
        context['tasks'] = tasks
        return context

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