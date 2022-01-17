from django.urls import path
from webapp.views import (HomePage, CreateTask, TaskView, UpdateTask, DeleteTask)


urlpatterns = [
    path('', HomePage.as_view(template_name='index.html'), name='home_page'),
    path('create/', CreateTask.as_view(), name='create_page'),
    path('task/<int:pk>', TaskView.as_view(template_name='view_page.html'), name='view_page'),
    path('update/<int:pk>', UpdateTask.as_view(template_name='update_task.html'), name='update_page'),
    path('delete/<int:pk>', DeleteTask.as_view(template_name='delete.html'), name='delete_page')
]