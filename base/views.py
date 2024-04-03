from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

# login logout authentication libraries
from django.contrib.auth.views import LoginView

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import login


from .models import Task


def Home(request):
    return render(request,"base/index.html")

def About(request):
    return render(request,"base/about.html")

def Services(request):
    return render(request,"base/services.html")

def Team(request):
    return render(request,"base/team.html")

def Contact(request):
    return render(request,"base/contact.html")

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')
    

class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


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

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__contains=search_input)
                # title__icontains
                # title__startswith

        context['search_input'] = search_input

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


# Page Not Found Error Handling Page
def handler404(request, exception):
    return render(request, '404.html', status=404)

# Internal Server Error Handling Page
def handler500(request):
    return render(request, '500.html', status=500)