from django.urls import path
from django.contrib import admin
from .views import ( 
    index, other_page, profile, user_activate, get_documents,
    TC_LoginView, TC_LogoutView, TC_PasswordChangeview, 
    TC_ChangeUserInfoView, TC_RegisterUserView, TC_RegisterDoneView       
)

app_name = 'app'

urlpatterns = [
    path('', index, name='index'),
    path('my-admin/', admin.site.urls),
    path('documents/', get_documents, name='documents'),
    path('accounts/register/activate/<str:sign>/', user_activate, name='register_activate'),
    path('accounts/register/done/', TC_RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', TC_RegisterUserView.as_view(), name='register'),
    path('accounts/logout/', TC_LogoutView.as_view(), name='logout'),
    path('accounts/password/change/', TC_PasswordChangeview.as_view(), name='password_change'),
    path('accounts/profile/change/', TC_ChangeUserInfoView.as_view(), name='profile_change'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/login/', TC_LoginView.as_view(), name='login'),
]