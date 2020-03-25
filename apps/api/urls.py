from django.urls import path, include

from . import views

urlpatterns = [
    path('auth/', include('apps.auth.urls')),

    path('user/my-details/', views.LoggedInUserDetailView.as_view()),
    path('user/details/<int:pk>/', views.UserDetailView.as_view()),
    path('user/ping/', views.UserPingView.as_view()),  # update 'last_action_dt'

    path('rooms/', views.RoomListCreateView.as_view()),
    path('rooms/<int:pk>/', views.RoomRetrieveUpdateView.as_view()),
]
