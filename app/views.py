from django.shortcuts import (
    render, get_object_or_404, HttpResponse
)
# from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.urls import reverse_lazy

from django.views.generic.edit import ( 
    CreateView, UpdateView, DeleteView
)
from django.views.generic.base import TemplateView

from django.template.loader import get_template

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView
)
from django.core.signing import BadSignature

from .models import AdvUser, Document
from .forms import ( 
    ChangeUserInfoForm, RegisterUserForm
)
from .utilities import signer

from rest_framework import viewsets
from .serializers import (
    AdvUserSerializer, DocumentSerializer 
)

# Create your views here.
def index(request):
    # Логика обработки запроса
    return render(request, 'app/index.html')

# Documents view start
@login_required
def get_documents(request):
    return render(request, 'app/documents.html')
    
# Documents view end
def get_about(request):
    return  render(request, 'app/about.html')

# Authentification / Registration / Activation / Delete (start)
@login_required
def profile(request):
    return  render(request, 'app/profile.html')

class TC_LoginView(LoginView):
    template_name = 'app/login.html'    
    
class TC_LogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'app/logout.html'    

class TC_ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AdvUser
    template_name = 'app/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy ('app:profile')
    success_message = 'Данные пользователя изменены'
    
    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)
    
    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)
    
class TC_PasswordChangeview(SuccessMessageMixin, LoginRequiredMixin,PasswordChangeView):
    template_name = 'app/password_change.html'
    success_url = reverse_lazy('app:profile')
    success_message = 'Пароль пользователя изменен'

class TC_RegisterUserView(CreateView):
    model = AdvUser
    template_name = 'app/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('app:register_done')  

class TC_RegisterDoneView(TemplateView):
    template_name = "app/register_done.html"
  
class TC_DeleteUserView(LoginRequiredMixin, DeleteView):
    model = AdvUser
    template_name = 'app/delete_user.html'
    success_url = reverse_lazy('app:index')
    
    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Пользователь удален')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)
  
def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'app/bad_signature.html')
    user = get_object_or_404(AdvUser, username=username)
    if user.is_activated:
        template = 'app/user_is_activated.html'
    else:
        template = 'app/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)    
# Authentification / Registration / Activation (end)

