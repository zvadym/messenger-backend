from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from . import views

urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('auth/token/logout/', views.TokenLogoutView.as_view(), name='token_verify'),

    path('user/details/', views.UserDetailView.as_view()),
    path('user/ping/', views.UserPingView.as_view()),  # update 'last_action_dt'
]
