from django.urls import path
from users_microservice import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from . import views

urlpatterns = [
	# Backend Methods:
	path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
	# CRUD and login/logout for user:
	path('register/', views.createUser, name="create-user"),
	path('signin/', views.login, name='login'),
	path('logout/', views.BlacklistRefreshView.as_view(), name="logout"),
	path('user/', views.user, name="user"),
	path('user/<str:pk>', views.user, name="user"),
	# Verify email:
	path('send-otp/', views.sendOTP, name='send-otp'),
	path('verify-otp/', views.verifyOTP, name='verify-otp'),
	# Admin methods
	path('getusers/', views.getUsers, name="get-users"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
