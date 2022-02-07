from django.urls import path

from issue_tracker.apps.accounts.views import login_view, logout_view
from issue_tracker.apps.webapp.views import (HomePage, CreateTask, TaskView, UpdateTask, DeleteTask)
from issue_tracker.apps.webapp.views.projects import ProjectPage, ProjectView, CreateProject, ProjectTaskCreate, UpdateProject, \
    DeleteProject

urlpatterns = [
    path('', HomePage.as_view(), name='home_page'),
    path('create/', CreateTask.as_view(), name='create_page'),
    path('task/<int:pk>', TaskView.as_view(), name='view_page'),
    path('update/<int:pk>', UpdateTask.as_view(), name='update_page'),
    path('delete/<int:pk>', DeleteTask.as_view(), name='delete_page'),
    path('projects/', ProjectPage.as_view(), name='project_page'),
    path('project/project_view<int:pk>', ProjectView.as_view(), name='project_view'),
    path('project/create/', CreateProject.as_view(), name='project_create'),
    path('project/<int:pk>/task/create', ProjectTaskCreate.as_view(), name='project_task_create'),
    path('project/<int:pk>/update', UpdateProject.as_view(), name='project_update'),
    path('project/<int:pk>/delete', DeleteProject.as_view(), name='project_delete'),
    path('accounts/login/', login_view, name='login'),
    path('accounts/logout/', logout_view, name='logout')
]