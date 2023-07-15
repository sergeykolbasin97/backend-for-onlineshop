from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext as _
from django.views import View
from django.views.generic import CreateView, UpdateView, DetailView, ListView, TemplateView

from myauth.models import Profile



class HelloView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        text = _('Hi')
        return HttpResponse(f'{ text }')

class AboutMeView(DetailView):
    template_name = 'myauth/about-me.html'
    model = Profile
    context_object_name = 'profile'

class AboutMeUpdateView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        return self.request.user.is_superuser

    model = Profile
    fields = 'bio', 'agreement_accepted', 'avatar'
    def get_success_url(self):
        return reverse(
            'myauth:about-me',
            kwargs={'pk': self.object.pk},
        )

class UserListView(ListView):
    template_name = 'myauth/users-list.html'
    model = User
    context_object_name = 'users'


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'myauth/register.html'
    success_url = reverse_lazy('myauth:users_list')
    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(self.request, username=username, password=password)
        login(request=self.request, user=user)
        return response

def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse('Сookie добавлены')
    response.set_cookie('lang', 'eng', max_age=5000)
    return response

def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get('lang', 'Cookie отсутствуют')
    return HttpResponse(f'Данные cookie: {value!r}')

def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session['Книга'] = 'Война и мир'
    return HttpResponse('Сессия добавлена')

def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get('Книга', 'Данные в сессии отсутствуют')
    return HttpResponse(f'Данные сессии: {value!r}')

class MyLogOutView(LogoutView):
    next_page = reverse_lazy('myauth:login')