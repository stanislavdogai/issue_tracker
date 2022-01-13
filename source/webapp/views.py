from django.shortcuts import render, get_object_or_404, redirect
from webapp.models import Task
from django.views import View
from django.views.generic import TemplateView, RedirectView
from webapp.forms import TaskForm, TaskFormDelete



class HomePage(View):
    def get(self, request, *args, **kwargs):
        tasks = Task.objects.order_by("summary")
        return render(request, 'index.html', {'tasks': tasks})

class TaskView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = get_object_or_404(Task, pk=kwargs.get("pk"))
        context['task'] = task
        return context

class CreateTask(View):
    def get(self, request, *args, **kwargs):
        form = TaskForm()
        return render(request, 'create_task.html', {'form' : form})

    def post(self, request, *args, **kwargs):
        form = TaskForm(data=request.POST)
        if form.is_valid():
            summary = form.cleaned_data.get('summary')
            description = form.cleaned_data.get('description')
            status = form.cleaned_data.get('status')
            type = form.cleaned_data.get('type')
            new_task = Task.objects.create(summary=summary,
                                           description=description,
                                           status=status,
                                           type=type)
            return redirect('view_page', new_task.pk)
        return render(request, 'create_task.html', {'form' : form})

class UpdateTask(TemplateView):
    def get(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs.get('pk'))
        form = TaskForm(initial={
            'summary' : task.summary,
            'status': task.status,
            'description': task.description,
            'type': task.type
        })
        return render(request, 'update_task.html', {'form' : form, 'task' : task})

    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs.get('pk'))
        form = TaskForm(data=request.POST)
        if form.is_valid():
            task.summary = form.cleaned_data.get('summary')
            task.description = form.cleaned_data.get('description')
            task.status = form.cleaned_data.get('status')
            task.type = form.cleaned_data.get('type')
            task.save()
            return redirect('view_page', task.pk)
        return render(request, 'create_task.html', {'form' : form})



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