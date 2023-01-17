from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('', views.getRoutes),

    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('register/', views.RegisterView.as_view(), name='register_user'),
    path('auth/google/', views.GoogleAuthApiView.as_view(), name='auth_google'),

    path('verify/mail/', views.EmailVerifyView.as_view(), name='user_activate'),
    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('forgot-password/verify/', views.ForgotPasswordVerifyView.as_view(), name='forgot_password-verify'),
    path('reset-password/', views.ResetPasswordView.as_view(), name='reset_password'),

    path('send-otp/', views.SendOtpView.as_view(), name='send_otp'),
    path('login-with-otp/', views.LoginWithOtpView.as_view(), name='login_with_otp'),

    path('profile/update/', views.profile_update, name='profile_update'),
    path('<str:username>/', views.profile, name='profile'),
    path('<str:username>/follow/', views.follow, name='follow'),
]