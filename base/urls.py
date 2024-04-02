from django.urls import path
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, DeleteView, CustomLoginView, RegisterPage, Home
from django.contrib.auth.views import LogoutView
from . import views


urlpatterns=[
    path('login/', CustomLoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('', views.Home, name="home"),
    path('about/', views.About, name="about"),
    path('services/', views.Services, name="services"),
    path('team/', views.Team, name="team"),
    path('contact/', views.Contact, name="contact"),
    path('tasks/',TaskList.as_view(), name="tasks"),
    path('task/<int:pk>',TaskDetail.as_view(), name="task"),
    path('task-create',TaskCreate.as_view(), name="task-create"),
    path('task-update/<int:pk>/',TaskUpdate.as_view(), name="task-update"),
    path('task-delete/<int:pk>/',DeleteView.as_view(), name="task-delete"),
]
