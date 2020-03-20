from django.urls import path, include

from . import views

urlpatterns = [
    path('auth/', include('apps.auth.urls')),

    path('user/details/', views.UserDetailView.as_view()),
    path('user/ping/', views.UserPingView.as_view()),  # update 'last_action_dt'
]
