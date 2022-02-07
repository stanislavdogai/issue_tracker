from django.urls import path

from accounts.views import login_view, logout_view
from webapp.views import (HomePage, CreateTask, TaskView, UpdateTask, DeleteTask)
from webapp.views.projects import ProjectPage, ProjectView, CreateProject, ProjectTaskCreate, UpdateProject, \
    DeleteProject

urlpatterns = [
    path('', HomePage.as_view(template_name='tasks/index.html'), name='home_page'),
    path('create/', CreateTask.as_view(), name='create_page'),
    path('task/<int:pk>', TaskView.as_view(template_name='tasks/view.html'), name='view_page'),
    path('update/<int:pk>', UpdateTask.as_view(template_name='tasks/update.html'), name='update_page'),
    path('delete/<int:pk>', DeleteTask.as_view(), name='delete_page'),
    path('projects/', ProjectPage.as_view(template_name='projects/index.html'), name='project_page'),
    path('project/project_view<int:pk>', ProjectView.as_view(template_name='projects/view.html'), name='project_view'),
    path('project/create/', CreateProject.as_view(), name='project_create'),
    path('project/<int:pk>/task/create', ProjectTaskCreate.as_view(), name='project_task_create'),
    path('project/<int:pk>/update', UpdateProject.as_view(), name='project_update'),
    path('project/<int:pk>/delete', DeleteProject.as_view(), name='project_delete'),
    path('accounts/login/', login_view, name='login'),
    path('accounts/logout/', logout_view, name='logout')
]