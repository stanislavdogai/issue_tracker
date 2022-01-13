from django.shortcuts import render, get_object_or_404, redirect
from webapp.models import Task
from django.views import View
from django.views.generic import TemplateView, RedirectView
from webapp.forms import TaskForm



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
            return redirect('home_page')
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
            task.summary = request.POST.get('summary')
            task.description = request.POST.get('description')
            task.status = request.POST.get('status')
            task.type = request.POST.get('type')
            task.save()
            return redirect('home_page')
        return render(request, 'create_task.html', {'form' : form})



class DeleteTask(View):
    pass