from django.urls import path
from .views import index, other_page, profile, user_activate, get_documents
from .views import TC_LoginView, TC_LogoutView, TC_PasswordChangeview, TC_ChangeUserInfoView, TC_RegisterUserView, TC_RegisterDoneView       

app_name = 'app'
urlpatterns = [
    path('documents/', get_documents, name='documents'),
    path('acoounts/register/activate/<str:sign>/', user_activate, name='register_activate'),
    path('acoounts/register/done/', TC_RegisterDoneView.as_view(), name='register_done'),
    path('acoounts/register/', TC_RegisterUserView.as_view(), name='register'),
    path('accounts/logout/', TC_LogoutView.as_view(), name='logout'),
    path('accounts/password/change/', TC_PasswordChangeview.as_view(), name='password_change'),
    path('accounts/profile/change/', TC_ChangeUserInfoView.as_view(), name='profile_change'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/login/', TC_LoginView.as_view(), name='login'),
    path('<str:page>/', other_page, name='other'),
    path('', index, name='index'),
]