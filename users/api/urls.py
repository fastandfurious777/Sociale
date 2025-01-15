from django.urls import path
from .views import (
    UserLoginApi,
    ResetPasswordRequestApi,
    ResetPasswordCheckApi,
    VerifyEmailApi,
    UserListApi,
    UserDetailApi,
    UserRegisterApi,
    UserUpdateApi,
    UserDeleteApi
)

app_name = 'users'

urlpatterns = [ 
    path('login/', UserLoginApi.as_view(), name='login'),
    path('register/', UserRegisterApi.as_view(), name='register'),
    path('verify-email/', VerifyEmailApi.as_view(), name='verify-email'),
    path('reset-password-request/', ResetPasswordRequestApi.as_view(), name='reset-password-request'),
    path('reset-password-check/', ResetPasswordCheckApi.as_view(), name='reset-password-check'),
    path('', UserListApi.as_view(), name='list'),
    path('<int:user_id>/', UserDetailApi.as_view(), name='detail'),
    path('<int:user_id>/update/', UserUpdateApi.as_view(), name='update'),
    path('<int:user_id>/delete/', UserDeleteApi.as_view(), name='delete'),
    
]