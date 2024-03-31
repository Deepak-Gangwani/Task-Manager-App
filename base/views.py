from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

# login logout authentication libraries
from django.contrib.auth.views import LoginView

from django.contrib.auth.mixins import LoginRequiredMixin


from .models import Task


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')

# Create your views here.
class TaskList(LoginRequiredMixin, ListView):
    model=Task
    # data storage custom variable name to pass data on template page
    context_object_name='tasks'
    # return HttpResponse("To Do List")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        # search_input = self.request.GET.get('search-area') or ''
        # if search_input:
        #     context['tasks'] = context['tasks'].filter(
        #         title__contains=search_input)

        # context['search_input'] = search_input

        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model=Task
    # data storage custom variable name to pass data on template page
    context_object_name='task'
    # changing the defualt name of taskdetail.html to task.html
    template_name='base/task.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    # fields='__all__'
    fields = ['title', 'description', 'complete']
    # redirect the form page to task page after submit
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    # fields='__all__'
    fields = ['title', 'description', 'complete']
    # redirect the form page to task page after submit
    success_url = reverse_lazy('tasks')


class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name='task'
    # fields='__all__'
    # redirect the form page to task page after submit
    success_url = reverse_lazy('tasks')