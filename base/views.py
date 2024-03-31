from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Task

# Create your views here.
class TaskList(ListView):
    model=Task
    # data storage custom variable name to pass data on template page
    context_object_name='tasks'
    # return HttpResponse("To Do List")


class TaskDetail(DetailView):
    model=Task
    # data storage custom variable name to pass data on template page
    context_object_name='task'
    # changing the defualt name of taskdetail.html to task.html
    template_name='base/task.html'


class TaskCreate(CreateView):
    model = Task
    fields='__all__'
    # redirect the form page to task page after submit
    success_url = reverse_lazy('tasks')
    # LoginRequiredMixin,
    # fields = ['title', 'description', 'complete']
    # success_url = reverse_lazy('tasks')

    # def form_valid(self, form):
    #     form.instance.user = self.request.user
    #     return super(TaskCreate, self).form_valid(form)


class TaskUpdate(UpdateView):
    model = Task
    fields='__all__'
    # redirect the form page to task page after submit
    success_url = reverse_lazy('tasks')


class DeleteView(DeleteView):
    model = Task
    context_object_name='task'
    # fields='__all__'
    # redirect the form page to task page after submit
    success_url = reverse_lazy('tasks')