# webapp/user/urls.py
from django.urls import path,include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django_rest_passwordreset.views import reset_password_confirm,reset_password_validate_token
from . import views

app_name = "user"

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='registration'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('token/', TokenObtainPairView.as_view(), name='access-token'),
    path('refresh-token/', TokenRefreshView.as_view(), name='refresh-token'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('password-forgot/', include('django_rest_passwordreset.urls', namespace='password_forgot')),
    path('password-forgot/confirm', reset_password_confirm, name='password_forgot_confirm'),
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('wallet/', views.WalletListCreateAPIView.as_view(), name='user-wallet'),
    path('wallet/admin', views.WalletAdminListAPIView.as_view(), name='admin-wallet'),
    # Admin API endpoints
    path('view-users/', views.UserListCreateAPIView.as_view(), name='view-users'),
    path('view-users/<uuid:uuid>/', views.UserRetrieveUpdateDestroyAPIView.as_view(), name='view-user'),
    path('user/reset-password', views.ResetUserPassword.as_view(), name="reset-user-password"),
    path('notifications/', views.NotificationListCreateAPIView.as_view(), name='notification-list-create'),

]