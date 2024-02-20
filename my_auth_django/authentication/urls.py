from django.urls import path, include
from django.contrib.auth import views as auth_views
from authentication import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='authentication/login.html', redirect_authenticated_user=True), name='login'),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('homepage/', views.homepage, name='homepage'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),

    # Password reset
    path('password_reset_confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='authentication/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='authentication/password_reset_done.html'), name='password_reset_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='authentication/password_reset.html'), name='password_reset'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='authentication/password_reset_complete.html'), name='password_reset_complete'),

]