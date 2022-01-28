from django.urls import path
from webapp.views import (HomePage, CreateTask, TaskView, UpdateTask, DeleteTask)


urlpatterns = [
    path('', HomePage.as_view(template_name='tasks/index.html'), name='home_page'),
    path('create/', CreateTask.as_view(), name='create_page'),
    path('task/<int:pk>', TaskView.as_view(template_name='tasks/view.html'), name='view_page'),
    path('update/<int:pk>', UpdateTask.as_view(template_name='tasks/update.html'), name='update_page'),
    path('delete/<int:pk>', DeleteTask.as_view(template_name='tasks/delete.html'), name='delete_page'),
]